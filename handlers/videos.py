import os
import ntpath
import utilities as utl
from send2trash import send2trash
from subprocess import Popen, PIPE
from ffmpy import FFmpeg, FFprobe


class Video:
    __tags = ['title', 'artist', 'album', 'track', 'genre', 'date', 'description', 'comment', 'grouping']
    __sets = {}  # Key=tag, Value=value for the tag
    __gets = {}  # Key=tag, Value=value for the tag
    __subs = {}  # Key=language, Value=subtitles path
    __chap = {}  # Key=ch start time, Value={title: title for ch, end: end time}

    def __init__(self, pathname):
        assert (ntpath.isdir(pathname) or ntpath.isfile(pathname)), "no file or directory %s exists" % pathname
        self.pathname = pathname
        self.videofiles = {}

        if ntpath.isfile(pathname):
            filename, extension = ntpath.basename(pathname).rsplit('.', 1)
            assert extension == "mp4", "file must be mp4 format"
            self.videofiles[pathname] = filename
            self.directory = ntpath.dirname(pathname)

        if ntpath.isdir(pathname):
            dir_files = utl.get_multiple(pathname, "mp4")
            assert dir_files, "no mp4 files in given directory"
            for file in dir_files:
                filename, extension = ntpath.basename(file).rsplit('.', 1)
                self.videofiles[file] = filename
            self.directory = pathname

        self.artwork = None
        self.clr = False

    def get_tag(self, tag):
        assert tag in self.__tags, '"%s" tag is not supported' % tag
        if tag not in self.__gets:
            result = []
            for file in self.videofiles:
                ff = FFprobe(
                    inputs={file: ['-v', 'error', '-show_entries', 'format_tags={}'.format(tag), '-of',
                                   'default=noprint_wrappers=1:nokey=1']}
                )
                with Popen(ff.cmd, stderr=PIPE, stdout=PIPE, shell=True) as proc:
                    file_tag = proc.communicate()[0].decode()[:-1]
                    result.append(file_tag if file_tag else None)

            if result and len(result) == 1:
                self.__gets[tag] = result[0]  # single file tag
            elif result:
                self.__gets[tag] = result  # list of tags
            else:
                self.__gets[tag] = None  # no tag was found

        return self.__gets[tag]

    def set_tag(self, tag, data):
        assert tag in self.__tags, '"%s" tag is not supported' % tag
        self.__sets[tag] = data
        self.__gets[tag] = data

    def add_subs(self, sub_path, lang):
        assert ntpath.isfile(sub_path), 'pathname "%s" does not belong to a file' % sub_path
        assert sub_path.rsplit(".", 1)[-1] == "srt", "subtitle must be srt"
        self.__subs[lang] = sub_path

    def set_artwork(self, img_path):
        assert ntpath.isfile(img_path), 'pathname "%s" does not belong to a file' % img_path
        assert img_path.rsplit(".", 1)[-1] == ("jpg" or "png"), "image must be jpg or png"
        self.artwork = img_path

    def add_chapter(self, start, end, title=None):
        sta_mili = utl.time_to_mili(start)
        end_mili = utl.time_to_mili(end) - 1
        self.__chap[sta_mili] = {'title': title, 'end': end_mili}

    def chapter_split(self, num_of_chapters):
        self.__chap.clear()
        duration = self.duration()
        ch_lenght = duration//num_of_chapters
        for i in range(num_of_chapters):
            start = ch_lenght*i
            end = ch_lenght*(i+1) - 1
            self.__chap[start] = {'title': "Chapter {}".format(i+1), 'end': end}

    def clear(self):
        self.clr = True
        self.artwork = None
        for tag in self.__tags:
            self.__sets[tag] = None
            self.__gets[tag] = None


    def rename(self, name):
        assert len(self.videofiles) == 1, "can't rename multiple files"
        self.videofiles[self.pathname] = name

    def save(self):
        inputs = {}  # dictionary for inputs as required by ffmpeg
        param = []  # ffmpeg output parameters

        #Video Clear
        param.append('-map_metadata')
        if self.clr:
            param.append('-1')
        else:
            param.append('-0')

        # tags parameters
        for tag in self.__sets:
            if self.__sets[tag]:
                param.extend(['-metadata', '{}={}'.format(tag, self.__sets[tag])])

        # artwork parameters
        if self.artwork:
            # adding the picture to the inputs
            inputs[self.artwork] = None
            # parameters for artwork as require by ffmpeg
            param.extend(['-map', '1', '-disposition:0', 'attached_pic'])

        # writing chapter file
        if self.__chap:
            ch_file = self.directory + "/My.Tag.Chapters.File.Writing"
            with open(ch_file, "w") as fp:
                fp.write(";FFMETADATA1\n")
                ch_num = 1
                for chapter in self.__chap:
                    fp.write("[CHAPTER]\nTIMEBASE=1/1000\n")
                    fp.write("START={}\nEND={}\n".format(chapter, self.__chap[chapter]['end']))

                    # If no title was specified we add "Chapter ch_num"
                    if self.__chap[chapter]['title']:
                        fp.write("title={}\n".format(self.__chap[chapter]['title']))
                    else:
                        fp.write("title=Chapter {}\n".format(ch_num))
                    ch_num += 1

            param.extend(['-map_metadata', str(len(inputs)+1)])
            inputs[ch_file] = None

        # copy the original streams to the output file
        param.extend(['-map', '0', '-c', 'copy'])

        # subtitles parameters
        if self.__subs:
            in_num = len(inputs) + 1
            sub_index = self.num_of_subs()
            for sub in self.__subs:
                inputs[self.__subs[sub]] = None
                param.extend(['-map', str(in_num), '-metadata:s:s:{}'.format(sub_index), 'language={}'.format(sub)])
                in_num += 1
                sub_index += 1
            param.append('-c:s')
            param.append('mov_text')

        signature = "[MyTag]"
        for file in self.videofiles:
            # Adding file path to the beginning of the inputs dictionary
            file_input = {file: ['-v', 'error']}
            file_input.update(inputs)

            # Setting file output name
            out_name = signature + self.videofiles[file] + '.mp4'
            output = os.path.join(self.directory, out_name)

            ff = FFmpeg(
                inputs=file_input,
                outputs={output: param}
            )
            print(ff.cmd)
            ff.run()  # execute ffmpeg command
            send2trash(file)  # send to trash the original file
            os.rename(output, file)
        if self.__chap:  # delete chapter file
            os.remove(ch_file)

    def duration(self):
        ff = FFprobe(
            inputs={self.pathname: ['-v', 'error', '-show_entries', 'format=duration', '-of',
                                    'default=noprint_wrappers=1:nokey=1']}
        )
        with Popen(ff.cmd, stderr=PIPE, stdout=PIPE, shell=True) as proc:
            mili_dur = round(float(proc.communicate()[0].decode())) * 1000
            return mili_dur

    def num_of_subs(self):
        # How many streams of subtitles the video has
        ff = FFprobe(
            inputs={self.pathname: ['-v', 'error', '-select_streams', 's', '-show_entries',
                                    'stream=index', '-of', 'default=noprint_wrappers=1:nokey=1']}
        )
        with Popen(ff.cmd, stderr=PIPE, stdout=PIPE, shell=True) as proc:
            sub_streams = proc.communicate()[0].decode().split()  # list of subtitles streams
            return len(sub_streams)
