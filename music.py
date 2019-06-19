import sdl_mixer 
import _sdl_mixer

_music=None

def load(file):
    global _music
    if _music:
        _sdl_mixer.Mix_FreeMusic(_music)
    _music=_sdl_mixer.Mix_LoadMUS(file)
    if not _music:
        raise sdl_mixer.sdl_mixer_error(_sdl_mixer.SDL_GetError())


def play():
    _sdl_mixer.Mix_PlayMusic(_music,0)

def get_busy():
    return _sdl_mixer.Mix_PlayingMusic()

def stop():
    _sdl_mixer.Mix_HaltMusic()

    

