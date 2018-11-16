import os
import ntpath
import pprint
import utilities as utl
import mutagen.id3 as mid3
from mutagen.easyid3 import EasyID3


class Audio:

    def __init__(self, pathname):
        assert (ntpath.isdir(pathname) or ntpath.isfile(pathname)), "no file or directory %s exists" % pathname
        self.pathname = pathname
        self.audiofiles = []
        self.tags = {}
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
        self.artwork = img_path

    def get_files(self):
        return [audio.filename for audio in self.audiofiles]

    def get_tag(self, tag):
        assert tag in EasyID3.valid_keys, '"%s" tag is not supported' % tag
        if tag in self.tags:
            return self.tags[tag]
        else:
            result = []
            for audio in self.audiofiles:
                file = EasyID3(audio)
                audio_tag = file.get(tag)[0]
                if audio_tag:
                    result.append(audio_tag)
            self.tags[tag] = result
        return self.tags[tag] if self.tags[tag] else None

    def set_tag(self, tag, data):
        assert tag in EasyID3.valid_keys, '"%s" tag is not supported' % tag
        self.tags[tag] = data

    def clear(self):
        self.clr = True

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
                tmp.add(mid3.GRP1(text=""))  # grouping frame
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
            for tag in self.tags:
                tmp[tag] = self.tags[tag]
                tmp.save()
