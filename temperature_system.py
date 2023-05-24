from perlin_noise import PerlinNoise

"""
Temperature System
"""

class TemperatureSystem():
  @staticmethod
  def setup():
    degreeOctives = 12
    degreeSeed = 2022
    TemperatureSystem.amp = 16
    TemperatureSystem.degFreq = 128
    
    TemperatureSystem.noisyTemp = PerlinNoise( octaves=degreeOctives, seed=degreeSeed )
    
  def genGlobalTemps(_x, _y, _z):
    temps = TemperatureSystem.noisyTemp([_x/TemperatureSystem.degFreq, _z/TemperatureSystem.degFreq])
    temps += abs(_y)
    temps *= TemperatureSystem.amp
    return temps
  
TemperatureSystem.setup()