class Helpers:
    @staticmethod
    def create_enumerate_song_list(args):
        enumerate_songs = {idx + 1: value for (idx, value) in enumerate(args)}
        return enumerate_songs

    @staticmethod
    def decode_list(args):
        args = [arg.decode("utf-8") for arg in args]
        return args
