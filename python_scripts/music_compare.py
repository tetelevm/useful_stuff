"""
Music Library Editor.
Needs detailed DOCSTRING and comments to the code, as it is strictly
dependent on the library structure.
"""

import os
from pathlib import Path
import shutil
import mutagen


PARENT_FOLDER = '/mnt/hard/'
FROM_FOLDER = 'music11'
TO_FOLDER = 'music'


def do_input(description='', args=('y', 'n')):
    msg = description + ' (<' + '>/<'.join(args) + '>): '
    answer = None
    while answer not in args:
        if answer is not None:
            print('unexpected input!')
        answer = input(msg)
    return answer


def set_or_log(audio, attr, value, path):
    def do_set():
        print(f'<{attr}>| {path} >>> {old_val}  |||  {value}')
        do = ''
        if attr == 'tracknumber':
            flag = False
            try:
                flag = int(value) == int(old_val.split('/')[0])
            except:
                pass

            do = 'y' if flag else do

        if not do:
            do = do_input('do set')

        if do == 'y':
            print('YES set')
            audio[attr] = value
            audio.save()
        else:
            print('NO set')
    try:
        if audio[attr][0] != value:
            old_val = audio[attr][0]
            do_set()
    except Exception as exc:
        old_val = f'<< no {attr} >>'
        do_set()


def check_meta(path: Path):
    fname = path.name
    falbum = path.parent.name
    fartist = path.parent.parent.name

    album = ' '.join(falbum.split(' ')[1:]).lstrip()
    title = '.'.join(fname.split('.')[1:-1]).lstrip()
    artist = fartist
    tracknumber = str(int(fname.split('.')[0]))
    date = falbum.split(' ')[0]

    try:
        audio = mutagen.File(path, easy=True)
    except Exception as exc:
        print(exc)
        print(path)
        return
    set_or_log(audio, 'album', album, path)
    set_or_log(audio, 'title', title, path)
    set_or_log(audio, 'date', date, path)
    set_or_log(audio, 'artist', artist, path)
    set_or_log(audio, 'albumartist', artist, path)
    set_or_log(audio, 'tracknumber', tracknumber, path)


class MusicMerger:
    def __init__(self, from_, to, base_dir=PARENT_FOLDER):
        self.base_dir = Path(base_dir)
        self.from_ = self.base_dir / from_
        self.to = self.base_dir / to

    def _create_arists(self):
        artist_of = {
            artist._parts[-1]
            for artist in self.from_.iterdir()
            if artist.is_dir()
        }
        artist_to = {
            artist._parts[-1]
            for artist in self.to.iterdir()
            if artist.is_dir()
        }
        self.not_artists = {
            artist._parts[-1]
            for artist in self.from_.iterdir()
            if not artist.is_dir()
        }

        self.artist_to_move = artist_of - artist_to - self.not_artists
        self.artist_to_check = artist_of - self.not_artists - self.artist_to_move

    def _create_albums(self):
        albums_of = {
            f'{album._parts[-2]}/{album._parts[-1]}'
            for artist in self.artist_to_check
            for album in (self.from_ / artist).iterdir()
            if album.is_dir()
        }
        albums_to = {
            f'{album._parts[-2]}/{album._parts[-1]}'
            for artist in self.artist_to_check
            for album in (self.to / artist).iterdir()
            if album.is_dir()
        }
        self.not_albums = {
            f'{album._parts[-2]}/{album._parts[-1]}'
            for artist in self.artist_to_check
            for album in (self.from_ / artist).iterdir()
            if not album.is_dir()
        }

        self.albums_to_move = albums_of - albums_to - self.not_albums
        self.albums_to_check = albums_of - self.not_albums - self.albums_to_move

    def _create_songs(self):
        songs_of = {
            f'{song._parts[-3]}/{song._parts[-2]}/{song._parts[-1]}'
            for album in self.albums_to_check
            for song in (self.from_ / album).iterdir()
            if self._is_song(song)
        }
        songs_to = {
            f'{song._parts[-3]}/{song._parts[-2]}/{song._parts[-1]}'
            for album in self.albums_to_check
            for song in (self.to / album).iterdir()
            if self._is_song(song)
        }
        self.not_songs = {
            f'{song._parts[-3]}/{song._parts[-2]}/{song._parts[-1]}'
            for album in self.albums_to_check
            for song in (self.from_ / album).iterdir()
            if not self._is_song(song)
        }

        self.songs_to_move = songs_of - songs_to - self.not_songs
        self.default_excesses = {
            song
            for song in self.not_songs
            if self._is_default_excess(song)
        }
        self.not_songs -= self.default_excesses

    def _calc_all_songs(self):
        all_artists = {
            artist
            for artist in self.to.iterdir()
            if artist.is_dir()
        }
        all_albums = {
            album
            for artist in all_artists
            for album in artist.iterdir()
            if album.is_dir()
        }
        self.all_songs = {
            song
            for album in all_albums
            for song in album.iterdir()
            if self._is_song(song, or_image=False)
        }

    # ================================================

    def _is_song(self, file, or_image=True):
        name = file._parts[-1]
        if name == 'cover.jpg' and or_image:
            return True
        if name.split('.')[-1] == 'mp3':
            return True
        return False

    def _is_default_excess(self, file):
        name = file.split('/')[-1]
        if name == 'desktop.ini':
            return True
        if name == 'AlbumArtSmall.jpg':
            return True
        if name == 'Folder.jpg':
            return True
        if name.startswith('AlbumArt_') and name.endswith('_Large.jpg'):
            return True
        if name.startswith('AlbumArt_') and name.endswith('_Small.jpg'):
            return True
        return False

    def _print_all(self):
        outliers = {
            f'artists to move from {self.from_}': self.artist_to_move,
            f'album to move from {self.from_}': self.albums_to_move,
            f'song to move from {self.from_}': self.songs_to_move,
            f'not artist in {self.from_}': self.not_artists,
            f'not album in {self.from_}': self.not_albums,
            f'default excesses in {self.from_}': self.default_excesses,
            f'smth excesses in {self.from_}': self.not_songs,
        }
        for (str_, list_) in outliers.items():
            if list_:
                print()
                print(str_)
                for smth in sorted(list_):
                    print(f'\t{smth}')

    def _remove_files(self, files):
        for file in files:
            os.remove(file)

    def _move_folder(self, folder):
        shutil.copytree(self.from_ / folder, self.to / folder)

    def _move_file(self, file):
        shutil.copy(self.from_ / file, (self.to / file).parent)

    def _move_artists(self):
        for artist in self.artist_to_move:
            self._move_folder(artist)

    def _move_albums(self):
        for album in self.albums_to_move:
            self._move_folder(album)

    def _move_files(self):
        for song in self.songs_to_move:
            self._move_file(song)

    def _check_metas(self):
        self._calc_all_songs()
        for song in sorted(list(self.all_songs)):
            check_meta(song)

    # ================================================

    def create_differents(self, said=True):
        self._create_arists()
        self._create_albums()
        self._create_songs()
        if said:
            self._print_all()

    def move_all(self):
        self._move_artists()
        self._move_albums()
        self._move_files()
        self._calc_all_songs()

    def check_meta(self):
        self._check_metas()


if __name__ == '__main__':
    merger = MusicMerger(from_=FROM_FOLDER, to=TO_FOLDER)
    merger.create_differents()
    if do_input('move files?') == 'y':
        merger.move_all()
        if do_input('check meta?') == 'y':
            merger.check_meta()
            print('All files checked!')
    else:
        print('Exit')
