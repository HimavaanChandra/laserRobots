class SoundFx():
    def __init__(self, filepath):
        from pygame import mixer
        mixer.init()
        self.filepath = filepath
        self.mixer = mixer
        self.music = self.mixer.music

    def play(self):
        self.music.load(self.filepath)
        self.music.play()

    def wait(self):
        while self.mixer.music.get_busy():
            continue

    def pause(self):
        self.music.pause()


def Main():
    kachow = SoundFx("kachow.wav")
    pew_pew = SoundFx("pew_pew.wav")
    bang_bang = SoundFx("bang_bang.wav")

    kachow.play()
    kachow.wait()
    pew_pew.play()
    pew_pew.wait()
    bang_bang.play()
    bang_bang.wait()


if __name__ == '__main__':
    Main()
