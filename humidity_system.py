from perlin_noise import PerlinNoise

"""
Humidity system
"""

class HumiditySystem():
  @staticmethod
  def setup():
    humidityOctaves = 8
    humiditySeed = 30
    HumiditySystem.amp = 128
    HumiditySystem.humFreq= 256
    HumiditySystem.noisyHumid = PerlinNoise(octaves = humidityOctaves, seed = humiditySeed )
  
  def genGolbalWater(_x, _y, _z):
    water = HumiditySystem.noisyHumid([_x/HumiditySystem.humFreq, _z/HumiditySystem.humFreq])
    water *= HumiditySystem.amp
    return abs(water)
  
HumiditySystem.setup()