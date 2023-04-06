# from ursina import Entity, load_model, Mesh, model
from ursina import *
from random import randrange

class MeshTerrain:
    def __init__(this):
        this.subsets = []
        this.numSubsets = 1
        this.subWidth = 128
        this.block = load_model('block.obj')
        this.textureAtlas = 'texture_atlas_3.png'
        for i in range(0, this.numSubsets):
            e = Entity(model = Mesh(), texture = this.textureAtlas)
            e.texture_scale*=64/e.texture.width
            this.subsets.append(e)
    def genTerrain(this):
        x = 0
        z = 0
        d = int(this.subWidth * 0.5)
        for k in range(-d, d):
            for j in range(-d, d):
                y = randrange(-1, 1)
                this.genBlock(x+k, y, z+j)
        this.subsets[0].model.generate()      
    def genBlock(this, _x, _y, _z):
        # Extend to the vertices of our model, or first subset
        model = this.subsets[0].model
        model.vertices.extend([Vec3(_x,_y,_z) + v for v in this.block.vertices])
        # texture atlas at coord for grass
        uu = 8
        uv = 7
        model.uvs.extend([Vec2(uu, uv) + u for u in this.block.uvs])
        