from perlin_noise import PerlinNoise

class Perlin:
    def __init__(this):
        this.seed = 123
        #differneces
        this.octaves = 4
        # how often things change /\ vs _/-\_
        this.freq = 64
        # how high or low
        this.amp = 12
        this.pNoise = PerlinNoise(seed=this.seed, octaves=this.octaves)
    def getHeight(this, _x, _z):
        y = 0 
        y = this.pNoise([_x/this.freq, _z/this.freq]) * this.amp
        return y
        
