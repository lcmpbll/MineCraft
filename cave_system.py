"""
Our cave system used by gen perlin function
"""


class Caves: 
  #a function created when ever we use this module
  def __init__(this):
    this.caveDic = {}
    this.buildCaves()
  def buildCaves(this):
    this.caveDic = { 'x9z9': -9, 'x10z9': -9, 'x11z9': -9, 'x12z9': -9  }
  def checkCave(this, _x, _z):
    tempStr = this.caveDic.get('x' + str(int(_x)) + 'z' + str(int(_z)))
    return tempStr
  def makeCave(this, _x, _z, _height):
    tempStr = this.caveDic.get('x' + str(int(_x)) + 'z' + str(int(_z)))
    this.caveDic[tempStr] = _height
  # def makeHill(this, _x, _z, _height):
  #   if(checkCave(_x, _z) != None)
  #   this.caveDic.update('x' + str(int(_x)) + 'z' + str(int(_z)) : += 1)
  
  
    