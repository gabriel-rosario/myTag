import ntpath
import os
from send2trash import send2trash
from subprocess import Popen, PIPE
from ffmpy import FFmpeg, FFprobe

class Video:
    __tags = ['title', 'artist', 'album', 'track', 'genre', 'date', 'description', 'comment', 'grouping']

    def __init__(self, pathname):
        assert ntpath.isfile(pathname), "given pathname doest not belong to a file"
        self.pathname = pathname
        self.filename, self.extension = ntpath.basename(pathname).rsplit('.', 1)
        self.directory = ntpath.dirname(pathname)
        self.metadata = {}
        self.subtitles = {}
        self.artwork = None

    # def load(self, pathname):
    #     assert ntpath.isfile(pathname), "given pathname doest not belong to a file"
    #     self.pathname = pathname
    #     self.filename, self.extension = ntpath.basename(pathname).rsplit('.', 1)
    #     self.directory = ntpath.dirname(pathname)
    #     self.metadata = {}

    def get_tag(self, tag):
        assert tag in self.__tags, "tag is not supported"
        ff = FFprobe(
            inputs={self.pathname: ['-v', 'error', '-show_entries', 'format_tags={}'.format(tag), '-of',
                                    'default=noprint_wrappers=1:nokey=1']}
        )
        with Popen(ff.cmd, stdout=PIPE, shell=True) as proc:
            return proc.communicate()[0].decode()

    def set_tag(self, tag, data):
        assert tag in self.__tags, "tag is not supported"
        self.metadata[tag] = data

    def add_subs(self, sub_path, lang):
        self.subtitles[lang] = sub_path

    def set_artwork(self, img_path):
        self.artwork = img_path

    def rename(self, name):
        self.filename = name

    def save_tags(self):
        # Setting file output name
        signature = "[MyTag]"
        out_name = signature + self.filename + '.' + self.extension
        output = os.path.join(self.directory, out_name)

        # Setting Inputs
        inputs = {self.pathname: ['-v', 'error']}

        # ffmpeg parameters
        param = []
        # metadata tags
        for tag in self.metadata:
            param.append('-metadata')
            param.append('{}={}'.format(tag, self.metadata[tag]))
        # artwork
        if self.artwork:
            art_param = ['-map', '1', '-map', '0', '-disposition:0', 'attached_pic']
            param += art_param
            inputs[self.artwork] = None
        param.append('-c')
        param.append('copy')

        # subs
        if self.subtitles:
            map = 2 if self.artwork else 1  # if there is artwork subtitles will begin at input 2 else 1
            sub_param = []
            for sub in self.subtitles:
                inputs[self.subtitles[sub]] = None
                sub_param.append('-map',)
                sub_param.append(str(map))
                map += 1
            sub_param.append('-c:s')
            sub_param.append('mov_text')
            param += sub_param


        ff = FFmpeg(
            # self.pathname: ['-v', 'error'], self.artwork: None
            inputs=inputs,
            outputs={output: param}
        )
        print(ff.cmd)
        ff.run()
        send2trash(self.pathname)
        new_path = output.replace(signature, '')
        os.rename(output, new_path)
        # self.pathname = new_path
        return new_path

    # def set_tag(self, tag, data):
    #     assert tag in self.__tags, "tag is not supported"
    #     output = "{}/{}.mytag.{}".format(self.directory, self.filename, self.extension)
    #     ff = FFmpeg(
    #         inputs={self.pathname: ['-v', 'error']},
    #         outputs={output: ['-metadata', '{}={}'.format(tag, data), '-c', 'copy']}
    #     )
    #     print(ff.cmd)

    # def add_artwork(self, img):
    #     # output = self.directory+'/'+self.filename+".mytag."+self.extension
    #     output = "{}/{}.mytag.{}".format(self.directory, self.filename, self.extension)
    #     ff = FFmpeg(
    #         inputs={self.pathname: ['-v', 'error'], img: None},
    #         outputs={output: ['-map', '1', '-map', '0', '-c', 'copy', '-disposition:0', 'attached_pic']}
    #     )
    #     print(ff.cmd)

    def add_subtitle(self, subs, language):
        output = "{}/{}.mytag.{}".format(self.directory, self.filename, self.extension)
        ff = FFmpeg(
            inputs={self.pathname: ['-v', 'error'], subs: None},
            outputs={output: ['-map', '0', '-map', '1', '-c', 'copy', '-c:s', 'mov_text', '-metadata:s:s:0',
                              'language={}'.format(language)]}
        )
        print(ff.cmd)
        ff.run()