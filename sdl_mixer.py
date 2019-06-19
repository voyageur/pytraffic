import _sdl_mixer
import music

class sdl_mixer_error(RuntimeError):
    pass

def init(frequency=_sdl_mixer.MIX_DEFAULT_FREQUENCY,
         format=_sdl_mixer.MIX_DEFAULT_FORMAT,
         channels=_sdl_mixer.MIX_DEFAULT_CHANNELS,
         chunksize=4096):
    result=_sdl_mixer.SDL_Init(_sdl_mixer.SDL_INIT_AUDIO)
    if result!=0:
        raise sdl_mixer_error(_sdl_mixer.SDL_GetError())
    result=_sdl_mixer.Mix_OpenAudio(frequency,format,channels,chunksize)
    if result!=0:
        raise sdl_mixer_error(_sdl_mixer.SDL_GetError())
        
    

class Sound:
    def __init__(self,file):
        self.__sound=_sdl_mixer.Mix_LoadWAV(file)
        if not self.__sound:
            raise sdl_mixer_error(_sdl_mixer.SDL_GetError())            

    def play(self):
        _sdl_mixer.Mix_PlayChannel(-1,self.__sound,0)

    def __del__(self):
        _sdl_mixer.Mix_FreeChunk(self.__sound)
        
