from ursina import Vec2

class SwirlEngine:
  def __init__(this, _subWidth):
    this.subWidth = _subWidth
    # set up
    #tracks position of subset being generated
    this.pos = Vec2(0,0)
    this.reset(this.pos.x, this.pos.y)
    #current direction 0-3
    this.cd = 0
    this.direction = [Vec2(0,1), Vec2(1,0), Vec2(0, -1), Vec2(-1, 0)]
  def changeDirection(this):
    if this.cd < 3:
      this.cd += 1
    else: 
      this.cd = 0
      this.iteration += 1
    if this.cd == 2:
      #this.run = (this.iteration * 2) -1
      this.run += 1
    elif this.cd == 0:
      this.run += 1
    # else: 
    #   this.run = (this.iteration * 2)
  def move(this):
    if this.count < this.run:
      # each movement is the movement of a subwidth
      this.pos.x += this.direction[this.cd].x * this.subWidth
      this.pos.y += this.direction[this.cd].y * this.subWidth
      this.count += 1
    else:
      this.count = 0
      this.changeDirection()
      this.move()
      
  def reset(this, _x, _z):
    this.pos.x = _x
    this.pos.y = _z
    this.run = 1
    this.iteration = 1
    this.count = 0
    
    
        
  