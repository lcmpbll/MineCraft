""""
Our tree system, it plants trees if appropiate 
used by gen perlin function
"""
from perlin_noise import PerlinNoise
from ursina import Entity, Vec3, color
 
class Trees:
  def __init__(this):
    this.noise = PerlinNoise(seed=4)
    # Parent of trees for optimization
    this.trees = Entity()
    this.treesCounter = 0
  def checkTree(this, _x, _y, _z):
    freq = 1.5
    amp = 100
    treeChance = ((this.noise([_x/freq, _z/freq]))*amp)
    if treeChance > 40:
      this.plantTree(_x, _y, _z)
  def plantTree(this, _x, _y, _z):
    from random import randint
    tree = Entity(model = None, position = Vec3(_x,_y,_z))
    crown = Entity(model ='cube', scale=6, y=9, color=color.green, collider = 'none')
    trunk = Entity(model='cube', scale_y=12, scale_x = 0.6, scale_z = 0.6,  color=color.brown, collider = 'box')
    crown.parent = trunk.parent = tree
    tree.y += 4
    tree.rotation_y = randint(3, 360)
    tree.parent = this.trees
    this.treesCounter += 1
    if this.treesCounter % 32 == 0:
      print('combine')
      this.trees.combine()
      this.trees.collider = this.trees.model
      
   
    
