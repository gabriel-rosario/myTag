import ntpath
import utilities as utl
import mutagen.id3 as mid3
from mutagen.easyid3 import EasyID3


class Audio:
    __tags = ['title', 'artist', 'album', 'albumartist', 'composer', 'genre', 'date', 'tracknumber', 'discnumber', 'bpm']
    __sets = {}
    __gets = {}
    def __init__(self, pathname):
        assert (ntpath.isdir(pathname) or ntpath.isfile(pathname)), "no file or directory %s exists" % pathname
        self.pathname = pathname
        self.audiofiles = []
        self.artwork = None
        self.clr = False

        if ntpath.isfile(pathname):
            extension = ntpath.basename(pathname).rsplit('.', 1)[-1]
            assert extension == "mp3", "file must be mp3 format"
            self.audiofiles.append(pathname)

        if ntpath.isdir(pathname):
            dir_files = utl.get_multiple(pathname, "mp3")
            assert dir_files, "No mp3 files in given directory"
            self.audiofiles.extend(dir_files)

    def set_artwork(self, img_path):
        assert ntpath.isfile(img_path), 'pathname "%s" does not belong to a file' % img_path
        extension = img_path.rsplit(".", 1)[-1]
        assert extension == "jpg" or extension == "png", "image must be jpg or png"
        self.artwork = img_path

    def get_files(self):
        return [audio.filename for audio in self.audiofiles]

    def get_tag(self, tag):
        assert tag in self.__tags, '"%s" tag is not supported' % tag
        if tag not in self.__gets:
            result = []
            for audio in self.audiofiles:
                file = EasyID3(audio)
                audio_tag = file.get(tag)
                if audio_tag:
                    result.append(audio_tag[0])
                else:
                    result.append(None)

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

    def clear(self):
        self.clr = True
        self.artwork = None
        for tag in self.__tags:
            self.__sets[tag] = None
            self.__gets[tag] = None

    def save(self):
        if self.clr:
            for file in self.audiofiles:
                tmp = mid3.ID3(file)
                tmp.clear()
                tmp.add(mid3.TIT2(text=""))  # title frame
                tmp.add(mid3.TPE1(text=""))  # artist frame
                tmp.add(mid3.TALB(text=""))  # album frame
                tmp.add(mid3.TPE2(text=""))  # album artist frame
                tmp.add(mid3.TCOM(text=""))  # composer frame
                tmp.add(mid3.TCON(text=""))  # genre frame
                tmp.add(mid3.TDRC(text=""))  # date frame
                tmp.add(mid3.TRCK(text=""))  # tracknumber frame
                tmp.add(mid3.TPOS(text=""))  # discnumber frame
                tmp.add(mid3.TBPM(text=""))  # bpm frame
                tmp.save()

        if self.artwork:
            with open(self.artwork, 'rb') as albumart:
                for file in self.audiofiles:
                    tmp = mid3.ID3(file)
                    tmp['APIC'] = mid3.APIC(
                        encoding=3,
                        mime='image/jpeg',
                        type=3, desc=u'Cover',
                        data=albumart.read()
                    )
                    tmp.save()
                    albumart.seek(0)

        for file in self.audiofiles:
            tmp = EasyID3(file)
            for tag in self.__sets:
                if self.__sets[tag]:
                    tmp[tag] = self.__sets[tag]
                    tmp.save()
