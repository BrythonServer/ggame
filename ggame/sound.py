try:
    from ggame.sysdeps import *
except:
    from sysdeps import *

class SoundAsset(object):
    """
    Class representing a single sound asset (sound file, such as .mp3 or .wav).
    """    
    def __init__(self, url):
        """
        Create a `ggame.SoundAsset` instance by passing in the URL or file name
        of the desired sound. Sound file formats may include `.wav` or `.mp3`, subject
        to browser compatibility. 
        """
        self.url = url
        """
        A string containing the url or name of the asset file.
        """

        
class Sound(object):
    """
    The `ggame.Sound` class represents a sound, with methods for controlling
    when and how the sound is played in the application.
    """

    def __init__(self, asset):
        """
        Pass a valid `ggame.SoundAsset` instance when creating a `ggame.Sound` object.
        """
        self.asset = asset
        """
        A reference to the `ggame.SoundAsset` instance.
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
        The `ggame.Sound.volume` property is a number ranging from 0-100, that 
        represents the volume or intensity of the sound when it is playing.
        """
        return self.SND.getVolume()
        
    @volume.setter
    def volume(self, value):
        self.SND.setVolume(value)
   