## PyTraffic -- GStreamer-based audio backend.
##
## Pure-Python implementation using GStreamer via gi.repository.Gst.
## Provides Sound (fire-and-forget effects) and a music player object.

import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GLib

Gst.init(None)


class MixerError(RuntimeError):
    pass


def init(frequency=44100, **kwargs):
    """Initialise audio (no-op: Gst.init already called at import)."""
    pass


def _probe_file(path):
    """Return True if GStreamer can decode *path*, False otherwise.

    We push to PAUSED (not just READY) so that decodebin actually negotiates
    a decoder — READY alone succeeds even for unsupported formats.
    A 2-second timeout is generous enough for local files.
    """
    pipe = Gst.parse_launch(
        'filesrc location="{}" ! decodebin ! fakesink'.format(
            path.replace('"', '\\"')))
    ret = pipe.set_state(Gst.State.PAUSED)
    if ret == Gst.StateChangeReturn.FAILURE:
        pipe.set_state(Gst.State.NULL)
        return False
    # Wait up to 2 s for the state change to complete.
    ret, _, _ = pipe.get_state(2 * Gst.SECOND)
    pipe.set_state(Gst.State.NULL)
    return ret != Gst.StateChangeReturn.FAILURE


# ---------------------------------------------------------------------------
# Sound effect — fire-and-forget playback of a single audio file.
# ---------------------------------------------------------------------------

class Sound:
    _active = []   # class-level list of in-flight pipelines

    def __init__(self, file):
        if not _probe_file(file):
            raise MixerError("Cannot decode sound file: {}".format(file))
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
        self._playing = False   # explicit flag; avoids get_state() race

    def load(self, file):
        if not _probe_file(file):
            raise MixerError("Cannot decode music file: {}".format(file))
        self.stop()
        pipeline = Gst.parse_launch(
            'filesrc location="{}" ! decodebin ! audioconvert ! audioresample'
            ' ! autoaudiosink'.format(file.replace('"', '\\"')))
        bus = pipeline.get_bus()
        bus.add_signal_watch()
        bus.connect('message', self._on_message)
        self._pipeline = pipeline

    def _on_message(self, bus, msg):
        if msg.type in (Gst.MessageType.EOS, Gst.MessageType.ERROR):
            if self._pipeline:
                self._pipeline.set_state(Gst.State.NULL)
            self._playing = False

    def play(self):
        if self._pipeline:
            self._pipeline.set_state(Gst.State.PLAYING)
            self._playing = True

    def stop(self):
        if self._pipeline:
            self._pipeline.set_state(Gst.State.NULL)
            self._pipeline = None
        self._playing = False

    def get_busy(self):
        return self._playing


music = _MusicPlayer()
