"""
System for mined blocks dropping collectable materials.
"""
from ursina import Entity, Vec2, load_model, load_texture
from config import minerals


# collectable dictionary, store present block position
# 
def drop_collectible(_blockType, _pos, _model, _texture):
    c = Entity(model=load_model('block.obj', use_deepcopy=True), texture=_texture )
    c.scale = 0.33
    c.position = _pos
    #wrap texture from texture atlas
    c.texture_scale *= 64/c.texture.width
    # uv info for texture wrap # list comprehension
    uu = minerals[_blockType][0]
    uv = minerals[_blockType][1]
    c.model.uvs = ([Vec2(uu, uv) + u for u in c.model.uvs])
    c.model.generate()
    