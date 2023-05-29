"""
System for mined blocks dropping collectable materials.
"""
from ursina import Entity, Vec2, Vec3, Vec4, load_model, destroy, Audio, Sequence, Func
from config import minerals
from random import random
from math import sin, floor
from inventory_system import Item, hotspots



# make collectible more translucent as it gets closer to being destroyed. 


#collectable dictionary, store present block position
# pop_audio = Audio('pop.mp3', autoplay=False, loop=False)
# pick_up_audio =  Audio('pickup.mp3', autoplay=False, loop=False)
# WIP change to class
class Collectible(Entity):
  #collectablesDic = {}

  def __init__(this, _blockType, _pos, _tex, _subject ):
    super().__init__()
    this.model = load_model('block.obj', use_deepcopy=True)
    this.original_position = _pos
    this.texture = _tex
    this.position = _pos
    this.subject = _subject
    this.numVerticies = len(this.model.vertices)
    this.blockType = _blockType
    this.collectables = []
    this.texture_scale *= 64/this.texture.width
    this.scale = 0.33
    this.shade = 1
    this.rotation_speed = 2
    # this.s = Sequence(120, Func(this.fade_out, duration=2), 2, Func(this.fade_in, duration=2), loop=True)
    # this.s.start()
    # record before adjusting position
    #Collectible.collectablesDic[this.position] = this
    this.y += 0.5 - (this.scale_y * 0.5)
    # put in after adjusting position
    this.original_y = this.position.y
    this.is_bouncing = True
    # sounds
    this.pick_up_audio =  Audio('pickup.mp3', autoplay=False, loop=False)
    this.pick_up_audio.pitch = 1 + random()
    this.pick_up_audio.volume = 1
    # mining sound
    e = Audio('pop.mp3', autoplay=False, loop=False)
    e.pitch = 1 + random()
    e.play()
    
    this.drop_collectible()
    
  def drop_collectible(this):
    uu = minerals[this.blockType][0]
    uv = minerals[this.blockType][1]
    
    if len(minerals[this.blockType]) > 2: 
      c = random() - 0.5
      ce = minerals[this.blockType][2]
      this.shade = ce[3]
      # replace colors instead of extending.
      this.model.colors = (   (Vec4(ce[0]-c,ce[1]-c,ce[2]-c,ce[3]),)* this.numVerticies)

    else: 
      c = random() - 0.5
      this.model.colors = ((Vec4(1 - c, 1 -c, 1- c, this.shade),)* this.numVerticies)
    
    this.model.uvs = ([Vec2(uu, uv) + u for u in this.model.uvs])
    # make sound
    
    this.model.generate()
    # destroy after some amount of time
    
    destroy(this, 120)
  def update(this):
    this.bounce()
    
    this.checkPickUp()
    this.degrade_collectables()
  
  def checkPickUp(this):
    # we need to keep checking where the subject is
    x = round(this.subject.position.x)
    y = floor(this.subject.position.y)
    z = round(this.subject.position.z)
    #if Collectible.collectablesDic.get((x, y, z)) != None:
    for i in range(0, 2):
      if y > this.subject.position.y + this.subject.height: return
      else:
        if Vec3(x, y, z) == this.original_position or Vec3(x, y + i, z) == this.original_position:
          if Item.new_item(this.blockType) == True:
            
            this.pick_up_audio.play()
            if this.subject.blockType == None:
              for h in hotspots:
                if h.onHotbar == False: continue
                if h.selected and h.item.blockType == this.blockType:
                  this.subject.blockType = this.blockType
            destroy(this)
            break
        
     
  def degrade_collectables(this):
    this.shade -= 0.0005
    this.rotation_speed += 0.002
    if this.shade <= 0:
      #Collectible.collectablesDic[this.position].pop()
      destroy(this)

      
  def bounce(this):
    # adds a small bounce
    this.rotation_y += this.rotation_speed
    if this.is_bouncing == True:
      this.y = (this.original_y + sin(this.rotation_y * 0.05)* this.scale_y)
      







    
    