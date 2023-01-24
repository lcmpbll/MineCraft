from ursina import Entity, color
from numpy import floor
# from cave_system import makeCave

class Mining_system: 

  def __init__(this, _subject, _camera, _subsets):
    this.grassStrokeTex = 'grass_mono.png'
    this.wireTex = 'wireframe.png'
    this.stoneTex = 'grass_mono.png'
    # store a reference of these here so we can use them in buildTool(), and elsewhere
    this.subject = _subject
    this.camera = _camera
    # subsets stored to reference in mining
    this.subsets = _subsets
    # Build tool entity --floating wire frame cube
    this.bte = Entity(model='cube', texture=this.wireTex, scale=1.01)
    this.build_distance = 3
    this.buildMode = -1 # -1 is off 1 is on
    #Our new block type system 
    this.blockTypes = []
    # Stone, Grass, Soil, Ruby, Netherite
    this.blockTypes.append(color.rgb(255, 255, 255))
    this.blockTypes.append(color.rgb(0, 255, 0))
    this.blockTypes.append(color.rgb(200, 100, 100))
    this.blockTypes.append(color.rgb(255, 0, 0))
    this.blockTypes.append(color.rgb(0, 0, 0))
    this.howManyBlockTypes = len(this.blockTypes)
    this.blockType = 0
    
    
  def input(this, key):
    if this.buildMode == 1:
      if key == 'left mouse up': 
        this.build()
      elif key == 'right mouse up':  ##else if
        this.mine()
      if key == 'f': this.buildMode *= -1
      if key == '1': this.blockType = 0
      if key == '2': this.blockType = 1
      if key == '3': this.blockType = 2
      if key == '4': this.blockType = 3
      if key == '5': this.blockType = 4
      if key == 'scroll up':
       this.build_distance += 1
      if key == 'scroll down':
        this.build_distance -= 1
    elif key == 'f': this.buildMode *= -1
    
  # Place a block at the bte posion 
  def build(this):
    if this.buildMode == -1:
      return
    e = Entity(model='cube', position= this.bte.position)
    e.collider = 'box'
    e.texture = this.grassStrokeTex
    e.color = this.blockTypes[this.blockType]
    e.shake(duration=0.5, speed=0.01)
  
  # This is called from the main update loop
  def buildTool(this): 
    # global build_distance
    if this.buildMode == -1:
      this.bte.visible = False
      return
    else: this.bte.visible = True
    
    this.bte.position = round(this.subject.position + this.camera.forward * this.build_distance)
    this.bte.y += 2
    this.bte.y = round(this.bte.y)
    this.bte.x = round(this.bte.x)
    this.bte.z = round(this.bte.z)
    this.bte.color = this.blockTypes[this.blockType]
    
  def mine(this):
    # e = mouse.hovered_entity
    # destroy(e)
    # iterate over all the subsets
    # s is an integer from 0 to subset length -1
    # v is the corners of each of the cubes in each of the cubes of the subsets
    # is the vertex close enought to where we want to mine? bte position
    for s in range(len(this.subsets)):
      vChange = False
      for v in this.subsets[s].model.vertices:
        if(v[0] >= this.bte.x - 0.5 and 
          v[0] <= this.bte.x + 0.5 and
          v[1] >= this.bte.y - 0.5 and
          v[1] <= this.bte.y + 0.5 and
          v[2] >= this.bte.z - 0.5 and
          v[2] <= this.bte.z + 0.5 ):
          #v[1] -= 1
          v[1] = 9999
          #Note that we have made change gather average height for cave ditionary
          vChange = True
      if vChange == True:
        this.subsets[s].model.generate()
        return 
        #anush.makeCave(bte.x, bte.z, bte.y-1)
    
  
    

     

  
  


 

  
