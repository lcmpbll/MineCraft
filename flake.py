from ursina import Entity, Vec3, time
from random import random


"""
Snow Flake Module : )
everything that an entity can do our flake can do 
Entity inheritance, can override inherited values with super
if you inherit from the from the Entity class in Ursina you can use an update function and it will be called automatically.
"""
class Flake(Entity):
  # This is a variable that does not belong to all instances of Flake
  sub = None
  # this is called a decorator, static means just one of these methods for the class.
  @staticmethod
  def setSub(_subjectEntity):
    Flake.sub = _subjectEntity
  def __init__(this, _origin):
    super().__init__(
      model='quad',
      texture='flake_1.png',
      position = _origin,
      scale = 0.5,
      double_sided = True,
    )
    this.randomDistance = random() * 40 -10
    this.minSpeed = 0.3
    this.minSpin = 10
    this.fallSpeed = random() * 4 + this.minSpeed
    this.visible = True
    this.spinSpeed = 4 * random() + this.minSpin
    # if this.y < 2:
    #   this.visible = False
    this.x += this.randomDistance
    this.z += this.randomDistance
    this.y += random()* 10 + 5
    # would be better to check if we've actually hit a terrain block
    # increase speed as you get higher?
  def update(this):
    this.physics() 
  def physics(this):
    _subPos = Flake.sub.position
    this.y -= this.fallSpeed * time.dt
    this.rotation_y += this.spinSpeed * time.dt
    if this.y > 15 and this.y < 50:
      this.fallSpeed = 10
    if this.y < _subPos.y -2 or this.y < -2:
      this.x = _subPos.x + this.getRandomDistance()
      this.z = _subPos.z + this.getRandomDistance()
      this.y =  random() * 10 + 5
    if _subPos.y < 2 and this.y < _subPos.y + 1:
      this.y = 55
      this.fallSpeed = 0
      # this.visible = False
    elif _subPos.y > 2:
      # when assigned above, they were all coming down in a line. 
      this.x = _subPos.x + this.getRandomDistance()
      this.z = _subPos.z + this.getRandomDistance()
      this.y =  random() * 10 + 5
  def getRandomDistance(this):
    return random() * 40 -10
# a control system for the snow flakes
class SnowFall():
  def __init__(this, _subref):
    this.flakes = []
    Flake.setSub(_subref)
    for i in range(128):
      e = Flake(_subref.position)
      this.flakes.append(e)
      