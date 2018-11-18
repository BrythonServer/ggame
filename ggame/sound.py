try:
    from ggame.sysdeps import *
except:
    from sysdeps import *

class SoundAsset(object):
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

        
class Sound(object):
    """
    The Sound class represents a sound, with methods for controlling
    when and how the sound is played in the application.
    
    :param SoundAsset asset: A valid :class:`SoundAsset` instance.
    
    :returns: the Sound instance
    """

    def __init__(self, asset):
        self.asset = asset
        """
        A reference to the sound asset instance.
        """
        self.SND = SND_Sound(self.asset.url)
        """
        A reference to the underlying sound object provided by the system.
        """
        self.SND.load()
        
    def play(self):
        """
        Play the sound once.
        """
        self.stop()
        self.SND.play()

    def loop(self):
        """
        Play the sound continuously, looping forever.
        """
        self.stop()
        self.SND.loop()
        self.SND.play()
        
    def stop(self):
        """
        Stop playing the sound.
        """
        self.SND.stop()
        
    @property
    def volume(self):
        """
        The volume property is a number ranging from 0-100 that 
        represents the volume or intensity of the sound when it is playing.
        """
        return self.SND.getVolume()
        
    @volume.setter
    def volume(self, value):
        self.SND.setVolume(value)
   