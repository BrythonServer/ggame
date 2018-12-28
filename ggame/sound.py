"""
Tools for loading and playing sound resources in ggame applications.
"""

from ggame.sysdeps import SND_Sound


class SoundAsset:
    """
    Class representing a single sound asset (sound file, such as .mp3 or .wav).

    :param str url: The URL or file name of the desired sound. Sound file
        formats may include `.wav` or `.mp3`, subject to browser compatibility.

    :returns: The asset instance
    """

    def __init__(self, url):
        self.url = url
        """
        A string containing the url or name of the asset file.
        """


class Sound(object):  # pylint: disable=useless-object-inheritance
    """
    The Sound class represents a sound, with methods for controlling
    when and how the sound is played in the application.

    :param SoundAsset asset: A valid :class:`SoundAsset` instance.

    :returns: the Sound instance
    """

    def __init__(self, asset):
        self._asset = asset
        """
        A reference to the sound asset instance.
        """
        self._snd = SND_Sound(self._asset.url)
        """
        A reference to the underlying sound object provided by the system.
        """
        self._snd.load()

    def play(self):
        """
        Play the sound once.
        """
        self.stop()
        self._snd.play()

    def loop(self):
        """
        Play the sound continuously, looping forever.
        """
        self.stop()
        self._snd.loop()
        self._snd.play()

    def stop(self):
        """
        Stop playing the sound.
        """
        self._snd.stop()

    @property
    def volume(self):
        """
        The volume property is a number ranging from 0-100 that
        represents the volume or intensity of the sound when it is playing.
        """
        return self._snd.getVolume()

    @volume.setter
    def volume(self, value):
        self._snd.setVolume(value)
