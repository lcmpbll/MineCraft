"""
System for mined blocks dropping collectable materials.
"""
from ursina import Entity, Vec2, Vec4, load_model, math, time
from config import minerals
from random import random
from math import sin




#collectable dictionary, store present block position

# WIP change to class
class Collectible(Entity):
  collectablesDic = {}

  def __init__(this, _blockType, _pos, _tex ):
    super().__init__()
    this.model = load_model('block.obj', use_deepcopy=True)
    this.texture = _tex
    this.position = _pos
    this.numVerticies = len(this.model.vertices)
    this.blockType = _blockType
    this.collectables = []
    this.texture_scale *= 64/this.texture.width
    this.scale = 0.33
    this.shade = 1
    this.timeStamp = time.time()
    # record before adjusting position
    Collectible.collectablesDic[this.position] = this
    this.y += 0.5 - (this.scale_y * 0.5)
    # put in after adjusting position
    this.original_y = this.position.y
    this.drop_collectible()
  def drop_collectible(this):
    uu = minerals[this.blockType][0]
    uv = minerals[this.blockType][1]
    
    if len(minerals[this.blockType]) > 2: 
      c = random() - 0.5
      ce = minerals[this.blockType][2]
      this.shade = ce[3]
      this.model.colors = (   (Vec4(ce[0]-c,ce[1]-c,ce[2]-c,ce[3]),)* this.numVerticies)

    else: 
      c = random() - 0.5
      this.model.colors = ((Vec4(1 - c, 1 -c, 1- c, this.shade),)* this.numVerticies)
    
    this.model.uvs = ([Vec2(uu, uv) + u for u in this.model.uvs])
    this.model.generate()
  def update(this):
    this.bounce()
    this.degrade_collectables()
    
     
  def degrade_collectables(this):
    this.shade -= 0.05
    if this.shade == 0:
      Collectible.collectablesDic[this] = None
      this.destroy()
      
  def bounce(this):
    # adds a small bounce
    this.rotation_y += 2
    this.y = (this.original_y + sin(this.rotation_y * 0.05)* this.scale_y)
  
      







    
    