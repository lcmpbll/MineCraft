
from ursina import Entity, floor, Mesh, Vec3, Vec2, Vec4, load_model, held_keys, mouse
from random import random
from perlin import Perlin
from swirl_engine import SwirlEngine
from mining_system import *
from building_system import checkBuild, gapShell
from config import six_cube_dir, minerals, mins
from tree_system import *

## WIP water flow
# check what happens to the block beneath when building
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
        
    
    def plantTree(this, _x, _y, _z):
        
      ent = TreeSystem.genTree(_x, _y, _z)
      treeH =  round(ent * 10)
      if ent == 0: 
        return 
      else:
        for i in range(treeH):
          # Trunk
          this.genBlock(_x, _y + i, _z, blockType='concrete')
        for t in range(-2, 3):
          for tt in range(4):
            for ttt in range(-2, 3):
            #crown
              this.genBlock(_x +  t, _y + treeH + tt, _z + ttt, blockType='emerald')
        
    def setup_subsets(this):
      # instanciate subset entities
      for i in range(0, this.numSubsets):
        e = Entity(model = Mesh(), texture = this.textureAtlas)
        e.texture_scale*=64/e.texture.width
        this.subsets.append(e)
    def do_mining(this):
      #pass in texture atlas for dropping collectable, see mine system
      epi = mine(this.terrainDic, this.vertexDic, this.subsets, this.textureAtlas, this.sub)
      if epi != None:
        this.genWalls(epi[0], epi[1])
        this.subsets[epi[1]].model.generate()
    def input(this, key):
      if key == 'left mouse up' and bte.visible == True and mouse.locked == True:
        this.do_mining()
      if key=='right mouse up' and bte.visible==True and mouse.locked == True:
        # do not build if empty handed.
        if this.sub.blockType is None: return
        buildSite = checkBuild( bte.position,
                                this.terrainDic,
                                this.cam.forward,
                                this.sub.position+Vec3(0,this.sub.height,0))
        if buildSite != None:
          this.genBlock(floor(buildSite.x), floor(buildSite.y), floor(buildSite.z), subset=0, building=True, blockType=this.sub.blockType)
          this.subsets[0].model.generate()
          gapShell(buildSite, this.terrainDic)
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
            this.genBlock(x+k, y, z+j)
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
        
        # decide random tint for color of block
        # c = random() - 0.5
        # model.colors.extend((Vec4(1-c, 1-c, 1-c, 1),) * this.numVertices)
        if blockType == 'soil':
            if _y > 2 and mining == False and building == False:
                # if random() > 0.86:
                #     blockType = 'stone'
                # elif random() > 0.9: 
                #     blockType = 'emerald'
                # elif random() > 0.95:
                #     blockType = 'ruby'
                # else:
                    blockType = 'snow'
            elif _y < -2 and building == False:
                if this.getDic(this.terrainDic, _x, _y + 1, _z) == 'g':
                    # We generated a gap when mining, decide what to fill it with, check for near by water
                    if this.checkForWater(_x, _y, _z, 'w'):
                    #or this.checkForWater(_x, _y, _z, 'water') == True:
                        blockType = 'water'
                        og_y = _y - 1
                        this.genWaterBlock(_x, _y + 1, _z, og_y)
                        
                    else: 
                        blockType = 'soil'
                else:
                    blockType = 'water'
                    og_y = _y
                    this.genWaterBlock(_x, _y + 1, _z, og_y)
                    
        
            elif mining == False and building == False:
                chance = random()
                if chance > 0.95:
                    blockType = 'ruby'
                elif chance > 0.9: 
                    blockType = 'emerald'
                elif chance > 0.85:
                    blockType = 'stone'
                else:
                    blockType = 'grass'
        
            elif mining == True: 
                chance = random()
                if chance > 0.95:
                    blockType = 'ruby'
                elif chance > 0.9: 
                    blockType = 'emerald'
                elif chance > 0.85:
                    blockType = 'stone'
                else:
                #soil
                    blockType = 'soil'
                # uu = 10
                # uv = 7
       
        uu = minerals[blockType][0]
        uv = minerals[blockType][1]
        # random tint for blocks
        c = random() -0.5
        # get Vec4 color data
        if len(minerals[blockType]) > 2:
            ce = minerals[blockType][2]
            # adjust each color channel separately to ensure hard-coded RGB combination is continued
            model.colors.extend((Vec4(ce[0] - c, ce[1]-c, ce[2] - c, ce[3]),) * this.numVertices)
        elif blockType == 'water':
            s = (abs(_y) /100) * 4
            model.colors.extend((Vec4( s,  s,  s, 0.5),) * this.numVertices)   
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
            
        if mining == False:
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
        if subset == -1:
            subset = this.currentSubset
        #figure out this posititioning
        wp = [
            Vec3(0, -1, 0),
            Vec3(1, 1 , 0),
            Vec3(-1, 1, 0),
            Vec3(0, 1, 1),
            Vec3(0, 1, -1),
            Vec3(1, -1, 0),
            Vec3(-1, -1, 0),
            Vec3(0, -1, -1)
        ]
        for i in range(0, 6):
            np  = cp + wp[i]
            if this.getDic(this.terrainDic, np.x, np.y, np.z ) == checkfor:
                isByWater = True
                break
        return isByWater
        
    def genWaterBlock(this, _x, _y, _z, og_y, subset=-1, mining = False):
        if subset == -1:
            subset = this.currentSubset
        if _y < -1:
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
            model.colors.extend((Vec4( c,  c,  c, 0.5),) * this.numVertices)
            # water coords
            uu = 9 
            uv = 7
            # if it is still deep do it again!
            if _y < -2 and mining == False:
                _y += 1
                this.genWaterBlock(_x, _y, _z, og_y)
            elif _y < -2 and mining == False and this.checkForWater(_x, _y, _z, 'g') == True: 
                _y += 1
                this.genWaterBlock(_x, _y, _z, og_y)
            model.uvs.extend([Vec2(uu, uv) + u for u in this.block.uvs])
    # After mining to create illusion of depth
    # soil is perhaps pass 
    

    
    def genWalls(this, epi, subset):
        if epi == None: return
        for i in range(0,6):
            np = epi + six_cube_dir[i]
            if this.getDic(this.terrainDic, np.x, np.y, np.z) == None:
                this.genBlock(np.x, np.y, np.z, subset, mining=True)

                

        
        
            
        
        