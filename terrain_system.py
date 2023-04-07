# from ursina import Entity, load_model, Mesh, model
from ursina import *
from random import randrange, random
from perlin import Perlin
from swirl_engine import SwirlEngine

class MeshTerrain:
    def __init__(this):
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
        this.perlin = Perlin()
        for i in range(0, this.numSubsets):
            e = Entity(model = Mesh(), texture = this.textureAtlas)
            e.texture_scale*=64/e.texture.width
            this.subsets.append(e)
    def getTerrainDic(this, _x, _y, _z):
        return this.terrainDic.get('x' + str(floor(_x)) + 'y' + str(floor(_y)) + 'z' + str(floor(_z)))
    def recTerrainDic(this, _x, _y, _z, _rec):
        this.terrainDic['x' + str(floor(_x)) + 'y' + str(floor(_y)) + 'z' + str(floor(_z))] = _rec
    def genTerrain(this):
        # get current position as we swirl around the world
        x = floor(this.swirlEngine.pos.x)
        z = floor(this.swirlEngine.pos.y)
        d = int(this.subWidth * 0.5)
        for k in range(-d, d):
            for j in range(-d, d):
                y = floor(this.perlin.getHeight(x+k, z+j))
                if this.getTerrainDic(x+k, y, z+j) == None:
                    this.genBlock(x+k, y, z+j)
        this.subsets[this.currentSubset].model.generate() 
        if this.currentSubset < this.numSubsets -1:
            this.currentSubset += 1 
        else:
            this.currentSubset = 0 
        this.swirlEngine.move()   
    def genBlock(this, _x, _y, _z):
        # Extend to the vertices of our model, or first subset
        model = this.subsets[this.currentSubset].model
        model.vertices.extend([Vec3(_x,_y,_z) + v for v in this.block.vertices])
        # record terrain in dictionary
        this.recTerrainDic(_x, _y, _z, "t")
        # decide random tint for color of block
        c = random() - 0.5
        model.colors.extend((Vec4(1-c, 1-c, 1-c, 1)) * this.numVertices)
        if _y > 2:
        # texture atlas at coord for grass
            uu = 8
            uv = 6
        elif _y < -2:
            uu = 9 
            uv = 7
        else:
            uu = 8
            uv = 7
        model.uvs.extend([Vec2(uu, uv) + u for u in this.block.uvs])
        