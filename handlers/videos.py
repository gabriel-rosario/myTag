import os
import ntpath
import utilities as utl
from send2trash import send2trash
from subprocess import Popen, PIPE
from ffmpy import FFmpeg, FFprobe


class Video:
    __tags = ['title', 'artist', 'album', 'track', 'genre', 'date', 'description', 'comment', 'grouping']

    def __init__(self, pathname):
        assert ntpath.isfile(pathname), 'pathname "%s" does not belong to a file' % pathname
        self.pathname = pathname
        self.filename, self.extension = ntpath.basename(pathname).rsplit('.', 1)
        self.directory = ntpath.dirname(pathname)
        self.metadata = {}  # Key=tag, Value=value for the tag
        self.subtitles = {}  # Key=language, Value=subtitles path
        self.chapters = {}  # Key=ch start time, Value={title: title for ch, end: end time}
        self.artwork = None

    def get_tag(self, tag):
        assert tag in self.__tags, '"%s" tag is not supported' % tag
        ff = FFprobe(
            inputs={self.pathname: ['-v', 'error', '-show_entries', 'format_tags={}'.format(tag), '-of',
                                    'default=noprint_wrappers=1:nokey=1']}
        )
        with Popen(ff.cmd, stderr=PIPE, stdout=PIPE, shell=True) as proc:
            tag = proc.communicate()[0].decode()
            return tag if tag else None

    def set_tag(self, tag, data):
        assert tag in self.__tags, '"%s" tag is not supported' % tag
        self.metadata[tag] = data

    def add_subs(self, sub_path, lang):
        assert ntpath.isfile(sub_path), 'pathname "%s" does not belong to a file' % sub_path
        assert sub_path.rsplit(".", 1)[-1] == "srt", "subtitles must srt"
        self.subtitles[lang] = sub_path

    def set_artwork(self, img_path):
        assert ntpath.isfile(img_path), 'pathname "%s" does not belong to a file' % img_path
        assert img_path.rsplit(".", 1)[-1] == ("jpg" or "png"), "image must be jpg or png"
        self.artwork = img_path

    def add_chapter(self, start, end, title=None):
        sta_mili = utl.time_to_mili(start)
        end_mili = utl.time_to_mili(end) - 1
        self.chapters[sta_mili] = {'title': title, 'end': end_mili}

    def chapter_split(self, num_of_chapters):
        self.chapters.clear()
        duration = self.duration()
        ch_lenght = duration//num_of_chapters
        for i in range(num_of_chapters):
            start = ch_lenght*i
            end = ch_lenght*(i+1) - 1
            self.chapters[start] = {'title': "Chapter {}".format(i+1), 'end': end}


    def rename(self, name):
        self.filename = name

    def save(self):
        # Setting file output name
        signature = "[MyTag]"
        out_name = signature + self.filename + '.' + self.extension
        output = os.path.join(self.directory, out_name)

        # Dictionary for inputs as required by ffmpeg
        inputs = {self.pathname: ['-v', 'error']}

        # ffmpeg output parameters
        param = []

        # tags parameters
        for tag in self.metadata:
            param.extend(['-metadata', '{}={}'.format(tag, self.metadata[tag])])

        # artwork parameters
        if self.artwork:
            # adding the picture to the inputs
            inputs[self.artwork] = None
            # parameters for artwork as require by ffmpeg
            param.extend(['-map', '1', '-map', '0', '-disposition:0', 'attached_pic'])

        # Writing chapter file
        if self.chapters:
            ch_file = self.directory + "/[CHAPTERS]" + self.filename
            with open(ch_file, "w") as fp:
                fp.write(";FFMETADATA1\n")
                ch_num = 1
                for chapter in self.chapters:
                    fp.write("[CHAPTER]\nTIMEBASE=1/1000\n")
                    fp.write("START={}\nEND={}\n".format(chapter, self.chapters[chapter]['end']))

                    # If no title was specified we add "Chapter ch_num"
                    if self.chapters[chapter]['title']:
                        fp.write("title={}\n".format(self.chapters[chapter]['title']))
                    else:
                        fp.write("title=Chapter {}\n".format(ch_num))
                    ch_num += 1

            param.extend(['-map_metadata', str(len(inputs))])
            inputs[ch_file] = None

        # copy the original streams to the output file
        param.extend(['-c', 'copy'])

        # subtitles parameters
        if self.subtitles:
            in_num = len(inputs)
            sub_index = self.num_of_subs()
            for sub in self.subtitles:
                inputs[self.subtitles[sub]] = None
                param.extend(['-map', str(in_num), '-metadata:s:s:{}'.format(sub_index), 'language={}'.format(sub)])
                in_num += 1
                sub_index += 1
            param.append('-c:s')
            param.append('mov_text')

        ff = FFmpeg(
            inputs=inputs,
            outputs={output: param}
        )
        print(ff.cmd)
        ff.run()  # execute ffmpeg command
        if self.chapters:  # delete chapter file
            os.remove(ch_file)
        send2trash(self.pathname)  # send to trash the original file
        self.pathname = output.replace(signature, '')  # erasing signature and setting new path
        os.rename(output, self.pathname)  # rename the copy file to the original file

    def duration(self):
        ff = FFprobe(
            inputs={self.pathname: ['-v', 'error', '-show_entries', 'format=duration', '-of',
                                    'default=noprint_wrappers=1:nokey=1']}
        )
        with Popen(ff.cmd, stderr=PIPE, stdout=PIPE, shell=True) as proc:
            mili_dur = round(float(proc.communicate()[0].decode()[:-2])) * 1000
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
