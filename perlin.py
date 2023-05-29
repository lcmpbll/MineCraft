from perlin_noise import PerlinNoise
from ursina import Text, destroy

class Perlin:
    def __init__(this):
        # og values ord('y') ord('o')
        this.seed = ord('y') + ord('o')
        # this.seed= 2022
        #differneces
        world  = Text(str(this.seed), scale=0.4)
        #destroy text on screen after 10 seconds. 
        destroy(world, 10)
        # 8
        this.octaves = 8
        # how often things change /\ vs _/-\_
        # 256
        this.freq = 256
        this.freq_continental = 512
        # how high or low
        # 24
        this.amp = 18
        this.amp_continental = 128
        this.pNoise_details = PerlinNoise(seed=this.seed, octaves=this.octaves)
        this.pNoise_continental = PerlinNoise(seed=this.seed, octaves=1)
    def getHeight(this, _x, _z):
        from math import sin
        y = 0 
        # add greater variation
        y = this.pNoise_continental([_x/this.freq_continental, _z/this.freq_continental]) * this.amp_continental
        y += this.pNoise_details([_x/this.freq, _z/this.freq]) * this.amp
        # follow a wave with surface variation
        sAmp = 0.33
        y += sin(_z) * sAmp
        y += sin(_x * 0.5) * sAmp
        return y
        
