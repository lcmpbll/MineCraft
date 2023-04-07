from ursina import Entity, color, floor
from dictionary_craft import DictionaryCraft
# class MiningSystem:
#     def __init__(this):
#       # this lots of red and green make yellow, 0.4 makes it shiny
bte = Entity(model='cube', color=color.rgba(1,1,0,0.4))
bte.scale = 1.001
parseDict = DictionaryCraft()
def highlight( pos, camera, terrainDic):
  for i in range(15, 1, -1):
    wp = pos + camera.forward * i 
    print(wp)
    x = floor(wp.x)
    y = floor(wp.y + 3)
    z = floor(wp.z)
    bte.y = y + 0.5
    bte.z = z
    bte.x = x
    if parseDict.getDictionary(terrainDic, x, y, z) == 't': 
      bte.visible  = True
      
      break
    else:
      bte.visible = False
def mine( terrainDic, vertexDic, subsets):
  if not bte.visible: return
        
      