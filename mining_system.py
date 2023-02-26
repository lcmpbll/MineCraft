from ursina import Entity, color, Vec3
# from numpy import floor
# from cave_system import makeCave

class Mining_system: 

  def __init__(this, _subject, _axe, _camera, _subsets ):
    this.grassStrokeTex = 'grass_mono.png'
    this.wireTex = 'wireframe.png'
    this.stoneTex = 'grass_mono.png'
    this.cubeModel = 'moonCube.obj'
    this.buildTex = 'build_texture.png'
    # store a reference of these here so we can use them in buildTool(), and elsewhere
    this.subject = _subject
    this.axe = _axe
    this.camera = _camera
    # Dictionary for recording position of terrain gaps
    this.tDic = {}
    # Entity for new builds
    this.builds = Entity(model=this.cubeModel, texture=this.buildTex)
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
        this.axe.shake(duration=1.3, magnitude=4, speed = 1, direction = (-5,.4))
        
        # this.axe.position = Vec3(0.3, -0.5, 2.8)
      elif key == 'right mouse up':  ##else if
        this.mine()
        this.axe.animate_position(value=Vec3(0.3, -0.5, 2.8), duration = 0.1)
        # this.axe.position = Vec3(0.3, -0.5, 2.8)
      # else: 
      #   #default axe position if not mining or building
      #   this.axe.position = Vec3(2, 0, 2.8)
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
    
  def mineSpawn(this):
    if this.tDic.get('x'+str(this.bte.x)+ 'y'+str(this.bte.y - 1)+ 'z'+str(this.bte.z)) == None:
      # record terrain change in dictionary
      this.tDic ['x'+str(this.bte.x)+ 'y'+str(this.bte.y)+ 'z'+str(this.bte.z)] = 'gap'
      
      #then we need to spawn a new cube in position where gaps are.
      e = Entity(model= this.cubeModel, texture = this.buildTex)
      #Makes cubes slightly smaller to allow for accurate verticies collection. 
      e.scale *= 0.99999
      # change color to soil
      e.color = this.blockTypes[2]
      #position under mine area
      e.position = this.bte.position
      e.y -= 1
      # parent spawned cube into builds entity.
      e.parent = this.builds
      #Record newly spawned block in dictionary
      this.tDic ['x'+str(this.bte.x)+ 'y'+str(e.y)+ 'z'+str(this.bte.z)] = e.y
      # Check for cave wall cubes, in areas that are not filled with terrain, no gaps, finally no terrain below position
      x = this.bte.x
      y = this.bte.Y
      z = this.bte.z
      pos1 = (x + 1, y, z)
      pos2 = (x -1, y, z)
      pos3 = (x, y, z + 1)
      pos4 = (x, y , z - 1)
      spawnPos = []
      spawnPos.append(pos1)
      spawnPos.append(pos2)
      spawnPos.append(pos3)
      spawnPos.append(pos4)
      for i in range(4):
        x = spawnPos[i][0]
        z = spawnPos[i][2]
        y = spawnPos[i][1]
        if this.tDic.get('x'+str(x)+ 'y'+str(y)+ 'z'+str(z)) == None and \
        this.tDic.get('x'+str(x)+ 'y'+str(y - 1)+ 'z'+str(z)) == None:
          e.position = spawnPos[i]
          e.parent = this.builds
          #Record newly spawned block in dictionary
          this.tDic ['x'+str(x)+ 'y'+str(y)+ 'z'+str(z)] = e.y
              #After swapnnning , update subset model and finish
              # also combine newly spawned blocks into builds entity
          this.builds.combine()
          
              
    
  # Place a block at the bte posion 
  def build(this):
    if this.buildMode == -1:
      return
    e = Entity(model= this.cubeModel, position= this.bte.position)
    #e.collider = 'box'
    e.texture = this.buildTex
    e.scale *= 0.99999
    # e.color = 4
    # e.texture = this.grassStrokeTex
    e.color = this.blockTypes[this.blockType]
    e.parent = this.builds
    # record new block in dictionary
    this.tDic ['x'+str(this.bte.x)+ 'y'+str(this.bte.y)+ 'z'+str(this.bte.z)] = 'b'
    this.builds.combine()
    # shaking wont work because we are destroying temp block in combining.
    # e.shake(duration=0.5, speed=0.01)
  
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
      totalV = 0
      for v in this.subsets[s].model.verticies:
        if(v[0] >= this.bte.x - 0.5 and 
          v[0] <= this.bte.x + 0.5 and
          v[1] >= this.bte.y - 0.5 and
          v[1] <= this.bte.y + 0.5 and
          v[2] >= this.bte.z - 0.5 and
          v[2] <= this.bte.z + 0.5 ):
          #Throw it up super high! To give illusion of mining. 
          v[1] = 9999
          
          vChange = True
          totalV += 1
      if vChange == True:
        buildBlock = True
        if this.tDic.get('x'+str(this.bte.x)+ 'y'+str(this.bte.y)+ 'z'+str(this.bte.z)) != 'b':
          # record new gap in dictionary should this be only if it isn't b? also should we delete the b from the tdic?
          this.tDic['x'+str(this.bte.x)+ 'y'+str(this.bte.y)+ 'z'+str(this.bte.z)] = 'gap'
          buildBlock = False
          this.mineSpawn()
          #update subsets model
        else:
          #might prevent gravity from doing it's thing
          this.tDic['x'+str(this.bte.x)+ 'y'+str(this.bte.y)+ 'z'+str(this.bte.z)] = 'nb'
        this.subsets[s].model.generate()
        if buildBlock == False: 
          this.builds.combine()
          
          # this.buids.combine()?
          # mystery of 36 verticies
          # print('tv=' + str(totalV))
      if totalV == 36: break
      return
            
      

    
  
    

     

  
  


 

  
