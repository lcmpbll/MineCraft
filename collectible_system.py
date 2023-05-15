"""
System for mined blocks dropping collectable materials.
"""
from ursina import Entity, Vec2, load_model, math
from config import minerals




#collectable dictionary, store present block position


collectables = []
# Dictionary to record where subject can pick up items
collectablesDic = {} 

def drop_collectible(_blockType, _pos, _texture):
  c = Entity(model=load_model('block.obj', use_deepcopy=True), texture=_texture )
  c.position = _pos
  collectablesDic[c.position]=_blockType
  print(collectablesDic.get((c.position)))
  c.scale = 0.33
  c.y += 0.5 - (c.scale_y * 0.5)
  #wrap texture from texture atlas
  c.texture_scale *= 64/c.texture.width
  # save og y for bouncing
  c.original_y = c.y
  # uv info for texture wrap # list comprehension
  uu = minerals[_blockType][0]
  uv = minerals[_blockType][1]
  if len(minerals[_blockType]) > 2: 
    c.color = minerals[_blockType][2]
  c.model.uvs = ([Vec2(uu, uv) + u for u in c.model.uvs])
  c.model.generate()
  collectables.append(c)
  
def collectible_bounce():
  for c in collectables: 
    c.rotation_y += 2
    c.y = (c.original_y + math.sin(c.rotation_y/50)* c.scale_y) 



#WIP change to class
# class Collectible:
#   def __init__(this):
#     this.collectables = []
#     this.model = load_model('block.obj', use_deepcopy=True)
    
#     this.c = Entity(model=this.model)
#   def drop_collectible(this, _blockType, _pos, _texture):
#     print(_blockType)
#     this.c.texture = _texture
#     this.c.position = _pos
#     this.c.texture_scale *= 64/this.c.texture.width
#     this.c.scale = 0.33
#     uu = minerals[_blockType][0]
#     uv = minerals[_blockType][1]
#     this.c.model.uvs = ([Vec2(uu, uv) + u for u in this.c.model.uvs])
#     this.c.model.generate()
#     this.collectables.append(this.c)
    
    