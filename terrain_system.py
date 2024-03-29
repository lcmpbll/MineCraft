
from ursina import Entity, floor, Mesh, Vec3, Vec2, Vec4, load_model, held_keys, mouse
# import random as rando
from perlin import Perlin
from swirl_engine import SwirlEngine
from mining_system import *
from building_system import checkBuild, gapShell
from config import six_cube_dir, minerals, mins
from tree_system import *
from inventory_system import *
# from temperature_system import *

## WIP water flow
# check what happens to the block beneath when building
# make better system for block selection
class MeshTerrain:
  def __init__(this, subject, cam):
    this.subsets = []
    this.numSubsets = 1024
    # passed in from main 
    this.sub = subject
    this.cam = cam
    # must be even see gen terrain
    this.subWidth = 6
    this.currentSubset = 0
    this.swirlEngine = SwirlEngine(this.subWidth)
    this.block = load_model('block.obj', use_deepcopy=True)
    this.textureAtlas = 'texture_atlas_3.png'
    this.numVertices = len(this.block.vertices)
    this.terrainDic = {}
    # our vertex dictionary  --- for mining
    this.vertexDic = {}
    this.perlin = Perlin()
    this.setup_subsets()
    
    # new planting/ planning terrain features
    this.featureFreq = 64
    this.featureAmp = 128
    this.tree_noise = PerlinNoise(octaves = 32, seed=2022)
      
  # def findTemp(this, _x, _y, _z):
  #   deg = TemperatureSystem.genGlobalTemps(_x, _y, _z)
  #   print(deg)
  #   return deg
        
  def plantStone(this, _x, _y, _z):
    stoneChance = this.tree_noise([_x/this.featureFreq, _z/this.featureFreq]) * this.featureAmp
    if stoneChance > 32:

      return True

    return False   
    
  def plantTree(this, _x, _y, _z):
      
    wiggle = floor(sin(_z*_x) * 3)
    wiggled_x = _x + wiggle
    wiggled_z = _z + wiggle
    wiggled_y = floor(this.perlin.getHeight(wiggled_x, wiggled_z))
    ent = TreeSystem.genTree(wiggled_x, wiggled_y, wiggled_z)
    habitability = 0
    tType = this.terrainDic.get((wiggled_x, wiggled_y, wiggled_z))
    if tType == 'soil' or tType == 'grass':
      growthFactor = rando.randint(2, 10)
    else: 
      growthFactor = rando.randint(1, 4)
    # add sin wave to grid
    treeH =  round(ent * growthFactor)
    # treeH = int(3 * ent)
    if ent == 0: 
      return 
    else:
      # add sin wave for x , z variability
      for i in range(treeH):
        # Trunk
        this.genBlock(wiggled_x, wiggled_y + i, _z, blockType='wood')
        if i < treeH:
          currentp = Vec3(wiggled_x, wiggled_y+i, wiggled_z )

          # for j in range(0,4):
          #   rt = currentp + four_square_dir[j]
            # if this.terrainDic.get((rt.x, rt.y, rt.z)) == None:
            #   this.recDic(this.terrainDic, rt.x, rt.y, rt.z, 'a')
      for t in range(-2, 3):
        for tt in range(4):
          for ttt in range(-2, 3):
          #crown
            # whatsH =this.terrainDic.get((wiggled_x +  t, wiggled_y + treeH + tt, wiggled_z + ttt))
            # if whatsH == None or whatsH == 'a':
              this.genBlock(wiggled_x +  t, wiggled_y + treeH + tt, wiggled_z + ttt, blockType='foilage')
            # if tt == 4:
            #   # add air to tops of trees
            #   this.recDic(this.terrainDic, _x +  t, _y + treeH + 1 + tt, _z + ttt, 'a')
            # if tt == 0: 
            #   if this.terrainDic.get(( _x +  t, _y + treeH -1 + tt, _z + ttt)) == None:
            #     this.recDic(this.terrainDic, _x +  t, _y + treeH -1 + tt, _z + ttt, 'a')
            # if t == -2:
            #   this.recDic(this.terrainDic, _x -1 +  t, _y + treeH  + tt, _z + ttt, 'a')
            # elif t == 3:
            #   this.recDic(this.terrainDic,  _x + 1 +  t, _y + treeH  + tt, _z + ttt, 'a' )
            # if ttt == -2:
            #   this.recDic(this.terrainDic, _x +  t, _y + treeH  + tt, _z + ttt -1, 'a')
            # elif ttt == 3:
            #   this.recDic(this.terrainDic,  _x  +  t, _y + treeH  + tt, _z + ttt + 1, 'a' )
              
      
  def setup_subsets(this):
    # instanciate subset entities
    for i in range(0, this.numSubsets):
      e = Entity(model = Mesh(), texture = this.textureAtlas)
      e.texture_scale*=64/e.texture.width
      this.subsets.append(e)
 
          
  def do_mining(this):
    #pass in texture atlas for dropping collectable, see mine system
    epi = mine(this.terrainDic, this.vertexDic, this.subsets, this.textureAtlas, this.sub)
    # return bte position and subset we are mining from.
    if epi != None and epi[2] != 'wood' and epi[2] != 'foilage':
      this.genWalls(epi[0], epi[1])
      
      this.subsets[epi[1]].model.generate()
  def input(this, key):
    if key == 'left mouse up' and bte.visible == True and mouse.locked == True:
      this.do_mining()
    if key=='right mouse up' and bte.visible==True and mouse.locked == True:
      # do not build if empty handed.
      if this.sub.blockType == None: return
      
      buildSite = checkBuild( bte.position,
                              this.terrainDic,
                              this.cam.forward,
                              this.sub.position+Vec3(0,this.sub.height,0))
      if buildSite != None:
        this.genBlock(floor(buildSite.x), floor(buildSite.y), floor(buildSite.z), subset=0, building=True, blockType=this.sub.blockType)
        this.subsets[0].model.generate()
        gapShell(buildSite, this.terrainDic)
        for h in hotspots:
          if h.onHotbar == False: continue
          # if h.item.blockType == this.sub.blockType:
          if h.selected == True:
            h.stack -= 1 
            h.item.update_stack_text()
            if h.stack < 1:
              destroy(h.item)
              h.occupied = False
              h.t.text = ''
              this.sub.blockType = None
            break
  def update(this):
    highlight(this.sub.position, this.sub.height, this.cam, this.terrainDic)
    #Blister mining == True
    if bte.visible and mouse.locked == True:
      #this is a for loop iterating over two variables
      if held_keys['shift'] and held_keys['left mouse']:
        this.do_mining()
  
        
                  
  def getDic(this, dic, _x, _y, _z):
    return dic.get((floor(_x), floor(_y), floor(_z)))
      
  def recDic(this, dic, _x, _y, _z, _rec):
    dic[(floor(_x), floor(_y), floor(_z))] = _rec
      
  def genTerrain(this):
    # get current position as we swirl around the world
    x = floor(this.swirlEngine.pos.x)
    z = floor(this.swirlEngine.pos.y)
    d = int(this.subWidth * 0.5)
    for k in range(-d, d):
      for j in range(-d, d):
        y = floor(this.perlin.getHeight(x+k, z+j))
        if this.getDic(this.terrainDic, x+k, y, z+j) == None:
          # decide blockType
          bType = 'grass'
          if this.plantStone(x+k, y, z+ j):
            bType = 'stone'
          if y > 2:
            bType = 'snow'
          if y < -2:
            bType = 'water'
          this.genBlock(x+k, y, z+j, blockType=bType)
          this.plantTree(x+k, y+1, z+j)
                
    this.subsets[this.currentSubset].model.generate() 
    if this.currentSubset < this.numSubsets -1:
      this.currentSubset += 1 
    else:
      this.currentSubset = 0 
    this.swirlEngine.move() 
  
  def genBlock(this, _x, _y, _z, subset=-1, mining=False, building=False, blockType='soil'):

      if subset == -1:
        subset = this.currentSubset
      # Extend to the vertices of our model, or first subset
      model = this.subsets[subset].model
      model.vertices.extend([Vec3(_x,_y,_z) + v for v in this.block.vertices])
      # if blockType == 'water':
   
      #   this.genWaterBlock(_x, _y , _z, _y, mining)
      if mining == True and _y > 0:
        blockType = 'soil'
      # elif mining == True:
      #   blockType = 'water'
      
      uu = minerals[blockType][0]
      uv = minerals[blockType][1]
      # random tint for blocks
      c = rando.random() -0.5
      # get Vec4 color data
      if len(minerals[blockType]) > 2:
        ce = minerals[blockType][2]
        # adjust each color channel separately to ensure hard-coded RGB combination is continued
        model.colors.extend((Vec4(ce[0] - c, ce[1]-c, ce[2] - c, ce[3]),) * this.numVertices)
      elif blockType == 'water':
        s = (abs(_y) /100) * 4
        model.colors.extend((Vec4( s,  s,  s, 1),) * this.numVertices) 
        this.genWaterBlock(_x, _y , _z, _y, mining)  
      else: 
        
        model.colors.extend((Vec4(1-c, 1-c, 1-c, 1),) * this.numVertices)

        
      model.uvs.extend([Vec2(uu, uv) + u for u in this.block.uvs])
      # record terrain in dictionary
      this.recDic(this.terrainDic, _x, _y, _z, blockType)
      # also record gap 
      if building == True:
          for i in range(0,6):
              checkPos = Vec3(_x, _y, _z) + six_cube_dir[i]
              if this.terrainDic.get((checkPos.x, checkPos.y, checkPos.z)) == None:
                  this.recDic(this.terrainDic, checkPos.x, checkPos.y, checkPos.z, 'a')
          
      if mining == False and blockType != 'water':
          if this.getDic(this.terrainDic, _x, _y + 1, _z) == None:
              this.recDic(this.terrainDic, _x, _y + 1, _z, 'a')
              
      # if building == True:
      #       #not sure if this is necessary
  
      #       if this.getDic(this.terrainDic, _x, _y + 1, _z) == None or this.getDic(this.terrainDic, _x, _y +1, _z) == 'g' :
      #         this.recDic(this.terrainDic, _x, _y + 1, _z, 'a')
      # record subet index and first vertext of the block. 
      vob = (subset, len(model.vertices) - this.numVertices - 1)
      this.recDic(this.vertexDic, _x, _y, _z, vob)
  

  def checkForWater(this, _x, _y, _z, checkfor, subset=-1):
      
    #can pass through water or air depending on initial generation or
    # Make ice?  
    cp = Vec3(_x, _y, _z)
    isByWater = False
    location = cp
    if subset == -1:
      subset = this.currentSubset
    for i in range(0, 4):
      np  = cp + four_square_dir[i]
      if this.getDic(this.terrainDic, np.x, np.y, np.z ) == checkfor:
        isByWater = True
        location = Vec3(np.x, np.y, np.z)
        break
    return (isByWater, location)
      
  def genWaterBlock(this, _x, _y, _z, og_y, subset=-1, mining = False):
    if subset == -1:
        subset = this.currentSubset
    # if _y < 0:
    # Extend to the vertices of our model, or first subset
    model = this.subsets[subset].model
    model.vertices.extend([Vec3(_x,_y,_z) + v for v in this.block.vertices])
    # record terrain in dictionary
    this.recDic(this.terrainDic, _x, _y, _z, "w")
    # record subet index and first vertext of the block. 
    # vob = (subset, len(model.vertices) - 37)
    # this.recDic(this.vertexDic, _x, _y, _z, vob)
    # decide random tint for color of block
    c = (abs(og_y) /100) * 4
    model.colors.extend((Vec4( c,  c,  c, .5),) * this.numVertices)
    # water coords
    uu = 9 
    uv = 7
    # if it is still deep do it again!

    if _y < -2 and mining == False:
      _y += 1
      this.genWaterBlock(_x, _y, _z, og_y)
    # elif _y < -2 and mining == False and this.checkForWater(_x, _y, _z, 'g')[0] == True: 
    #   _y += 1
    #   this.genWaterBlock(_x, _y, _z, og_y)
    # elif _y < -2 and mining == True and this.checkForWater(_x, _y, _z, 'g')[0] == True:
    #   wp = this.checkForWater(_x, _y, _z, 'g')[1]
    #   this.genWaterBlock(wp.x, wp.y, wp.z, og_y)
    # else:
    #   return
    model.uvs.extend([Vec2(uu, uv) + u for u in this.block.uvs])
  # After mining to create illusion of depth
  # soil is perhaps pass 
  

  
  def genWalls(this, epi, subset):
      if epi == None: return
      for i in range(0,6):
        np = epi + six_cube_dir[i]
        if this.getDic(this.terrainDic, np.x, np.y, np.z) == None:
          this.genBlock(np.x, np.y, np.z, subset, mining=True)

              

      
      
          
      
      