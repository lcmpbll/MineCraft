from perlin_noise import PerlinNoise
"""
Our tree system
"""

class TreeSystem():
    # def __init__(this, _x, _y, _z):
    #   this.x = _x
    #   this.y = _y
    #   this.z = _z
      
      
      
  
  @staticmethod
  def setup():
      Toctaves = 32
      treeSeed = 2022
      # how frequently the trees peter out. 
      TreeSystem.treeFreq = 64
      
      TreeSystem.noisyEnt = PerlinNoise(octaves=Toctaves, seed=treeSeed )
      # TreeSystem.genTree(_x, _y, _z)
    #create perlin noise method
    
  def genTree(_x, _y, _z):
  # check wether to generate a tree here
    if _y < -1: return 0
    ent = 1 + TreeSystem.noisyEnt([_x/TreeSystem.treeFreq, _z/TreeSystem.treeFreq])
    
    if ent > 1.435:
      return ent
    else:
      return 0
    
TreeSystem.setup()