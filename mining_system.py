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
  
  def tDicGet(this, x_, y_, z_):
     return this.tDic.get('x'+ str(x_)+ 'y'+ str(y_)+ 'z'+ str(z_)) 

  def tDicRec(this, x_, y_, z_, rec):
     this.tDic['x'+ str(x_)+ 'y'+ str(y_)+ 'z'+ str(z_)] = rec
    
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
      # if key == '-':
      #   this.bteHeight(-1)
      # if key == '=':
      #   this.bteHeight(1)
    elif key == 'f': this.buildMode *= -1
    
  def mineSpawn(this):
    if this.tDicGet(this.bte.x, this.bte.y -1, this.bte.z) == None:
      #this.tDic.get('x'+str(this.bte.x)+ 'y'+str(this.bte.y - 1)+ 'z'+str(this.bte.z)) == None:
      # record terrain change in dictionary, will do later
      # this.tDic ['x'+str(this.bte.x)+ 'y'+str(this.bte.y)+ 'z'+str(this.bte.z)] = 'gap'
      
      
      e = Entity( model=this.cubeModel,
                    texture=this.buildTex)
      # Shrink spawned block so that it
      # matches the size of ordinary terrain.
      e.scale *= 0.99999
      # Change colour to soil (this.blockTypes[2]).
      e.color = this.blockTypes[0]
      # Position under mined area.
      e.position = this.bte.position
      e.y -= 1
      # Parent spawned cube into builds entity.
      e.parent = this.builds
      
      
      # Record newly spawned block on dictionary.
        
      #then we need to spawn a new cube in position where gaps are.
      #e = Entity(model= this.cubeModel, texture = this.buildTex)
      #Makes cubes slightly smaller to allow for accurate verticies collection. 
      # e.scale *= 0.99999
      # # change color to soil
      # e.color = this.blockTypes[0]
      # #position under mine area
      # e.position = this.bte.position
      # e.y -= 1
      # # parent spawned cube into builds entity.
      # e.parent = this.builds
      #Record newly spawned block in dictionary
      this.tDicRec(this.bte.x, e.y, this.bte.z, e.y)
      # this.tDic['x'+str(this.bte.x)+ 'y'+str(e.y)+ 'z'+str(this.bte.z)] = e.y
      # Check for cave wall cubes, in areas that are not filled with terrain, no gaps, finally no terrain below position
      # x = this.bte.x
      # y = this.bte.Y
      # z = this.bte.z
      # pos1 = (x + 1, y, z)
      # pos2 = (x -1, y, z)
      # pos3 = (x, y, z + 1)
      # pos4 = (x, y , z - 1)
      # spawnPos = []
      # spawnPos.append(pos1)
      # spawnPos.append(pos2)
      # spawnPos.append(pos3)
      # spawnPos.append(pos4)
      # for i in range(4):
      #   x = spawnPos[i][0]
      #   z = spawnPos[i][2]
      #   y = spawnPos[i][1]  
      # 
      x = this.bte.x
      y = this.bte.y
      z = this.bte.z
      pos1 = (x+1,y,z)
      pos2 = (x-1,y,z)
      pos3 = (x,y,z+1)
      pos4 = (x,y,z-1)
      spawnPos = []
      spawnPos.append(pos1)
      spawnPos.append(pos2)
      spawnPos.append(pos3)
      spawnPos.append(pos4)
      for i in range(4):
          x = spawnPos[i][0]
          z = spawnPos[i][2]
          y = spawnPos[i][1]s
      
      if this.tDicGet(x, y, z) == None and \
        this.tDicGet(x, y - 1, z) == None:
      # if this.tDic.get('x'+str(x)+ 'y'+str(y)+ 'z'+str(z)) == None and this.tDic.get('x'+str(x)+ 'y'+str(y - 1)+ 'z'+str(z)) == None:
        e = Entity(model=this.cubeModel, texture=this.buildTex)
        e.scale *= 0.99999
        e.color= this.blockTypes[this.blockType]
        e.position = spawnPos[i]
        e.parent = this.builds
        #Record newly spawned block in dictionary
        this.tDicRec(x, y, z, e.y)
        #this.tDic ['x'+str(x)+ 'y'+str(y)+ 'z'+str(z)] = e.y
            #After swapnnning , update subset model and finish
            # also combine newly spawned blocks into builds entity
        # this.builds.combine()
  
  # def mineSpawn(this):
  #       # Spawn one block below dig position?
  #       if this.tDic.get(   'x'+str(this.bte.x)+
  #                           'y'+str(this.bte.y-1)+
  #                           'z'+str(this.bte.z)
  #                           ) == None:

  #           """
  #           # Record gap location in dictionary.
  #           this.tDic[  'x'+str(this.bte.x)+
  #                       'y'+str(this.bte.y)+
  #                       'z'+str(this.bte.z)] = 'gap'
  #           """

  #           e = Entity( model=this.cubeModel,
  #                       texture=this.buildTex)
  #           # Shrink spawned block so that it
  #           # matches the size of ordinary terrain.
  #           e.scale *= 0.99999
  #           # Change colour to soil (this.blockTypes[2]).
  #           e.color = this.blockTypes[0]
  #           # Position under mined area.
  #           e.position = this.bte.position
  #           e.y -= 1
  #           # Parent spawned cube into builds entity.
  #           e.parent = this.builds
  #           # Record newly spawned block on dictionary.
  #           this.tDic[  'x'+str(this.bte.x)+
  #                       'y'+str(e.y)+
  #                       'z'+str(this.bte.z)] = e.y

  #           # OK -- now spawn 4 'cave wall' cubes.
  #           # For each cube, first check whether:
  #           # 1) No terrain there already
  #           # 2) No gaps
  #           # 3) No terrain below this pos

                    
  #               # We can ask None both times because
  #               # this covers both gaps and terrain
  #               # being in these positions (i.e
  #               # potential cave wall and below
  #               # potential cave wall.
  #               if this.tDic.get(   'x'+str(x)+
  #                                   'y'+str(y)+
  #                                   'z'+str(z)
  #    a                   ) == None and \
  #                       this.tDic.get(  'x'+str(x)+
  #                                       'y'+str(y-1)+
  #                                       'z'+str(z)
  #                       ) == None:
  #                           e = Entity( model=this.cubeModel,
  #                                       texture=this.buildTex)
  #                           # Shrink spawned block so that it
  #                           # matches the size of ordinary terrain.
  #                           e.scale *= 0.99999
  #                           # Change colour to soil (this.blockTypes[2]).
  #                           e.color = this.blockTypes[0]
  #                           # Position around mined area.
  #                           e.position = spawnPos[i]
  #                           # Parent spawned cube into builds entity.
  #                           e.parent = this.builds
  #                           # Record newly spawned block on dictionary.
  #                           this.tDic[  'x'+str(x)+
  #                                       'y'+str(y)+
  #                                       'z'+str(z)] = e.y
        
              
    
  # Place a block at the bte posion 
  def build(this):
    if this.buildMode == -1:
      return
    # is there a block already here?
    whatsHere = this.tDic.get( 'x'+str(this.bte.x)+
                        'y'+str(this.bte.y)+
                        'z'+str(this.bte.z)) 
    if whatsHere != 'gap' and whatsHere != None:
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

    vChange = False
    totalV = 0 
    #WIP prevent crash when no block
    try:
      for v in this.builds.model.vertices:
          # Is the vertex close enough to
          # where we want to mine (bte position)?
          if (v[0] >=this.bte.x - 0.5 and
              v[0] <=this.bte.x + 0.5 and
              v[1] >=this.bte.y - 0.5 and
              v[1] <=this.bte.y + 0.5 and
              v[2] >=this.bte.z - 0.5 and
              v[2] <=this.bte.z + 0.5):

              # Move vertex high into air to
              # give illusion of being destroyed.
              v[1] = 9999
              # Note that we have made change.
              vChange = True
              totalV += 1
              if totalV >= 36 : break
    except:
       print('build not defined')
    if vChange == True:            
      #whatsHere = this.tDic( 'x'+str(this.bte.x)+
                        # 'y'+str(this.bte.y)+
                        # 'z'+str(this.bte.z)) 
      whatsHere = this.tDicGet(this.bte.x, this.bte.y, this.bte.z)
      if whatsHere !='b' :
          this.mineSpawn()
          this.builds.combine()
        #update builds models Entity so that we see gaps -- update verticies
      this.builds.model.generate()
      # Not done! Also combine newly spawned blocks
      # into builds entity :)
      return  

    # Our real mining of the terrain :) if not mining blocks
    # Iterate over all the subsets that we have...
    totalV = 0
    for s in range(len(this.subsets)):
      vChange = False 
      for v in this.subsets[s].model.vertices:
        if (v[0] >=this.bte.x - 0.5 and
            v[0] <=this.bte.x + 0.5 and
            v[1] >=this.bte.y - 0.5 and
            v[1] <=this.bte.y + 0.5 and
            v[2] >=this.bte.z - 0.5 and
            v[2] <=this.bte.z + 0.5):
                # Yes!
                # Move vertex high into air to
                # give illusion of being destroyed.
                v[1] = 9999
                # Note that we have made change.
                # Gather average height for cave dic.
                vChange = True
                # Record new gap on dictionary.
                # this.tDic[  'x'+str(this.bte.x)+
                #             'y'+str(this.bte.y)+
                #             'z'+str(this.bte.z)] = 'gap'
                totalV += 1
                # The mystery of 36 vertices!! :o
                
                if totalV==36: break
        
      if vChange == True:

        # Now we need to spawn a new cube below
        # the bte's position -- if no cube or
        # gap there already.
        # Next, spawn 4 cubes to create illusion
        # of more layers -- if each position is
        # neither a gap nor a place where terrain
        # already is.
        # Record new gap on dictionary.
        this.tDic[  'x'+str(this.bte.x)+
              'y'+str(this.bte.y)+
              'z'+str(this.bte.z)] = 'gap'
        this.mineSpawn()
        # Now that we've spawned what (if anything)
        # we need to, update subset model. Done.
        this.subsets[s].model.generate()
        this.builds.combine()
        return
  
  
  






