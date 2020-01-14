# coding=utf-8
from json import JSONEncoder

from obj.audio_obj import AudioObj


class DefaultDecoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, AudioObj):
            return o.__str__()
