from perlin_noise import PerlinNoise
"""
Our tree system
"""

class TreeSystem():
    # def __init__(this, _x, _y, _z):
    #   this.x = _x
    #   this.y = _y
    #   this.z = _z
      
      
      
  
  @staticmethod # not calling lots of instances, just this one method
  def setup():
    Toctaves = 8
    treeSeed = 2022
    TreeSystem.amp = 10
    # how frequently the trees peter out. 
    TreeSystem.treeFreq = 256
    
    TreeSystem.noisyEnt = PerlinNoise(octaves=Toctaves, seed=treeSeed )
    # TreeSystem.genTree(_x, _y, _z)
    #create perlin noise method
    
  def genTree(_x, _y, _z):
  # check wether to generate a tree here
    if _x % 3 == 0: return 0
    if _x % 5 == 0: return 0
    if _x % 7 == 0: return 0
   
  
  
    if _z % 3 == 0: return 0
    if _z % 5 == 0: return 0
    if _z % 11 == 0: return 0
  
    if _y < -1: 
      environment = 5
    elif _y > 2:
      environment = 3
    else:
      environment = 1
      
    ent = TreeSystem.noisyEnt([_x/TreeSystem.treeFreq, _z/TreeSystem.treeFreq])
    ent *= TreeSystem.amp
    
    if ent > environment:
      return ent
    else:
      return 0
    
TreeSystem.setup()