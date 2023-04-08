#from ursina import *
from ursina import Entity, floor, Mesh, Vec3, Vec2, Vec4, load_model
from random import randrange, random
from perlin import Perlin
from swirl_engine import SwirlEngine
from mining_system import *


class MeshTerrain:
    def __init__(this, pos, cam):
        this.subsets = []
        this.numSubsets = 128
        # must be even see gen terrain
        this.subWidth = 4
        this.currentSubset = 0
        this.swirlEngine = SwirlEngine(this.subWidth)
        this.block = load_model('block.obj')
        this.textureAtlas = 'texture_atlas_3.png'
        this.numVertices = len(this.block.vertices)
        this.terrainDic = {}
        # our vertex dictionary  --- for mining
        this.vertexDic = {}
        this.perlin = Perlin()
       
        for i in range(0, this.numSubsets):
            e = Entity(model = Mesh(), texture = this.textureAtlas)
            e.texture_scale*=64/e.texture.width
            this.subsets.append(e)
    def input(this, key):
        if key == 'left mouse up':
           epi = mine(this.terrainDic, this.vertexDic, this.subsets)
           this.genWalls(epi[0], epi[1])
           this.subsets[epi[1]].model.generate()
    def update(this, pos, cam):
        
        highlight(pos, cam, this.terrainDic)
    def getDic(this, dic, _x, _y, _z):
        return dic.get('x' + str(floor(_x)) + 'y' + str(floor(_y)) + 'z' + str(floor(_z)))
    def recDic(this, dic, _x, _y, _z, _rec):
        dic['x' + str(floor(_x)) + 'y' + str(floor(_y)) + 'z' + str(floor(_z))] = _rec
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
        this.subsets[this.currentSubset].model.generate() 
        if this.currentSubset < this.numSubsets -1:
            this.currentSubset += 1 
        else:
            this.currentSubset = 0 
        this.swirlEngine.move()   
    def genBlock(this, _x, _y, _z, subset=-1):
        if subset == -1:
            subset = this.currentSubset
        # Extend to the vertices of our model, or first subset
        model = this.subsets[subset].model
        model.vertices.extend([Vec3(_x,_y,_z) + v for v in this.block.vertices])
        # record terrain in dictionary
        this.recDic(this.terrainDic, _x, _y, _z, "t")
        # also recodr gap 
        if this.getDic(this.terrainDic, _x, _y + 1, _z) == None:
            this.recDic(this.terrainDic, _x, _y + 1, _z, 'g')
        # record subet index and first vertext of the block. 
        vob = (subset, len(model.vertices) - 37)
        this.recDic(this.vertexDic, _x, _y, _z, vob)
        # decide random tint for color of block
        c = random() - 0.5
        model.colors.extend((Vec4(1-c, 1-c, 1-c, 1),) * this.numVertices)
        if _y > 2:
        # texture atlas at coord for grass
            uu = 8
            uv = 6
        elif _y < -2:
            if this.getDic(this.terrainDic, _x, _y, _z) == 'g':
                if this.checkForWater(_x, _y, _z) == True:
                    uu = 9 
                    uv = 7
                    og_y = _y
                    this.genWaterBlock(_x, _y + 1, _z, og_y)
                else: 
                    uu = 10
                    uv = 7
            uu = 9 
            uv = 7
            og_y = _y
            this.genWaterBlock(_x, _y + 1, _z, og_y)
        else:
            uu = 8
            uv = 7
        model.uvs.extend([Vec2(uu, uv) + u for u in this.block.uvs])
    def checkForWater(this, _x, _y, _z, subset=-1):
        cp = Vec3(_x, _y, _z)
        isByWater = False
        if subset == -1:
            subset = this.currentSubset
        wp = [
                Vec3(1, 0 , 0),
                Vec3(-1, 0, 0),
                Vec3(0, 0, 1),
                Vec3(0, 0, -1)
        ]
        for i in range(0, 4):
            this.getDic(this.terrainDic, )
        
    def genWaterBlock(this, _x, _y, _z, og_y, subset=-1):
        if subset == -1:
            subset = this.currentSubset
        if _y < -1:
            if subset == -1:
                subset = this.currentSubset
            # Extend to the vertices of our model, or first subset
            model = this.subsets[subset].model
            model.vertices.extend([Vec3(_x,_y,_z) + v for v in this.block.vertices])
            # record terrain in dictionary
            this.recDic(this.terrainDic, _x, _y, _z, "w")
            # record subet index and first vertext of the block. 
            # vob = (subset, len(model.vertices) - 37)
            # this.recDic(this.vertexDic, _x, _y, _z, vob)
            # decide random tint for color of block
            c = abs(og_y) /100
            model.colors.extend((Vec4(0.75 + c, 0.75 + c, 0.75 + c, 0.5),) * this.numVertices)
            # water coords
            uu = 9 
            uv = 7
            # if it is still deep do it again!
            if _y < -2:
                _y += 1
                this.genWaterBlock(_x, _y, _z, og_y)
            # else:
            #     uu = 8
            #     uv = 7
            model.uvs.extend([Vec2(uu, uv) + u for u in this.block.uvs])
    # After mining to create illusion of depth
    def genWalls(this, epi, subset):
        if epi == None: return
        #wall position
        wp = [
                Vec3(0,1,0),
                Vec3(0,-1,0),
                Vec3(0,0,1),
                Vec3(0,0,-1),
                Vec3(1,0,0),
                Vec3(-1,0,0)
        ]
        for i in range(0,6):
            np = epi + wp[i]
            if this.getDic(this.terrainDic, np.x, np.y, np.z) == None:
                this.genBlock(np.x, np.y, np.z, subset)
        
            
        
        