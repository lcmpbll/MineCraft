"""
Our cave system used by gen perlin function
"""
from perlin_noise import PerlinNoise

class Caves: 
  #a function created when ever we use this module
  def __init__(this):
    this.caveDic = {}
    this.buildCaves()
  def buildCaves(this):
    this.caveDic = { 'x9z9': 'cave', 'x10z9': 'cave', 'x11z9': 'cave', 'x12z9': 'cave'  }
  def checkCave(this, _x, _z):
    if this.caveDic.get('x' + str(int(_x)) + 'z' + str(int(_z))) == 'cave':
      return True
    else: 
      return False