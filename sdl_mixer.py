## PyTraffic -- GStreamer-based audio backend.
##
## Replaces the old _sdl_mixer C extension (SDL 1.x) with a pure-Python
## implementation that uses GStreamer via gi.repository.Gst.  The public
## API is identical to the old sdl_mixer module so no other files need
## changing.

import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GLib

Gst.init(None)


class sdl_mixer_error(RuntimeError):
    pass


def init(frequency=44100, **kwargs):
    """Initialise audio (no-op: Gst.init already called at import)."""
    pass


# ---------------------------------------------------------------------------
# Sound effect — fire-and-forget playback of a single OGG/WAV file.
# ---------------------------------------------------------------------------

class Sound:
    _active = []   # class-level list of in-flight pipelines

    def __init__(self, file):
        # Probe that the file is actually playable.
        probe = Gst.parse_launch(
            'filesrc location="{}" ! decodebin ! fakesink'.format(
                file.replace('"', '\\"')))
        ret = probe.set_state(Gst.State.READY)
        if ret == Gst.StateChangeReturn.FAILURE:
            probe.set_state(Gst.State.NULL)
            raise sdl_mixer_error("Cannot load sound file: {}".format(file))
        probe.set_state(Gst.State.NULL)
        self._file = file

    def play(self):
        """Play the sound once, non-blocking."""
        pipeline = Gst.parse_launch(
            'filesrc location="{}" ! decodebin ! audioconvert ! audioresample'
            ' ! autoaudiosink'.format(self._file.replace('"', '\\"')))

        def _on_message(bus, msg, pipe):
            if msg.type in (Gst.MessageType.EOS, Gst.MessageType.ERROR):
                pipe.set_state(Gst.State.NULL)
                try:
                    Sound._active.remove(pipe)
                except ValueError:
                    pass
            return True

        bus = pipeline.get_bus()
        bus.add_signal_watch()
        bus.connect('message', _on_message, pipeline)
        pipeline.set_state(Gst.State.PLAYING)
        Sound._active.append(pipeline)


# ---------------------------------------------------------------------------
# Music player — streaming background music with load/play/stop/get_busy.
# ---------------------------------------------------------------------------

class _MusicPlayer:
    def __init__(self):
        self._pipeline = None

    def load(self, file):
        self.stop()
        self._pipeline = Gst.parse_launch(
            'filesrc location="{}" ! decodebin ! audioconvert ! audioresample'
            ' ! autoaudiosink'.format(file.replace('"', '\\"')))
        bus = self._pipeline.get_bus()
        bus.add_signal_watch()
        bus.connect('message', self._on_message)

    def _on_message(self, bus, msg):
        if msg.type in (Gst.MessageType.EOS, Gst.MessageType.ERROR):
            self._pipeline.set_state(Gst.State.NULL)

    def play(self):
        if self._pipeline:
            self._pipeline.set_state(Gst.State.PLAYING)

    def stop(self):
        if self._pipeline:
            self._pipeline.set_state(Gst.State.NULL)
            self._pipeline = None

    def get_busy(self):
        if self._pipeline is None:
            return False
        _, state, _ = self._pipeline.get_state(0)
        return state == Gst.State.PLAYING


music = _MusicPlayer()
