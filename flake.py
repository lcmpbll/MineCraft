from ursina import Entity, Vec3, time
from random import random


"""
Snow Flake Module : )
everything that an entity can do our flake can do 
Entity inheritance, can override inherited values with super

"""
class Flake(Entity):
  def __init__(this, _origin):
    super().__init__(
      model='quad',
      texture='flake_1.png',
      position = _origin,
      scale = 0.5,
      double_sided = True,
    )
    this.minSpeed = 0.6
    this.minSpin = 10
    this.fallSpeed = random() * 4 + this.minSpeed
    this.visible = True
    this.spinSpeed = 4 * random() + this.minSpin
    # if this.y < 2:
    #   this.visible = False
    this.x += random()* 40 -10
    this.z += random()* 40 -10
    this.y += random()* 10 + 5
    # would be better to check if we've actually hit a terrain block
    # increase speed as you get higher?
    
  def physics(this, _subPos):
    this.y -= this.fallSpeed * time.dt
    this.rotation_y += this.spinSpeed * time.dt
    if this.y > 15 and this.y < 50:
      this.fallSpeed = 10
    if this.y < _subPos.y or this.y < -2:
      this.x = _subPos.x + random()* 40 -10
      this.z = _subPos.z + random()* 40 -10
      this.y =  random()* 10 + 5
    if _subPos.y < 2 and this.y < -1:
      this.y = 55
      this.fallSpeed = 0
    elif _subPos.y > 2:
      this.x = _subPos.x + random()* 40 -10
      this.z = _subPos.z + random()* 40 -10
      this.y =  random()* 10 + 5