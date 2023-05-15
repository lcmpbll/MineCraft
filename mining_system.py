from ursina import Entity, color, floor, Vec3, load_model
from dictionary_craft import DictionaryCraft
from collectible_system import *

# class MiningSystem:
#     def __init__(this): not a class ?
# this lots of red and green make yellow, 0.4 makes it shiny
bteModel =  'block.obj' #load_model('block.obj', use_deepcopy=True)
bte = Entity(model=bteModel, color=color.rgba(1,1,0,0.4))
# suggested 1.1 and 0.05
bte.scale = 1.02
bte.origin_y += 0.01
parseDict = DictionaryCraft()

def highlight( pos, camera, terrainDic):
  # some times I fall through the terrain after building
  # we should look after this behaviour in a dedicated collectable class
  collectible_bounce()
  for i in range(1, 32):
    #adjust for player's height
    wp = pos + Vec3(0, 1.86, 0) + camera.forward * (i * 0.5)
    #round to improve accuracy,  can still be improved
    x = round(wp.x)
    y = floor(wp.y)
    z = round(wp.z)
    bte.y = y 
    # + 0.5
    bte.z = z
    bte.x = x
    whatT = parseDict.getDictionary(terrainDic, x, y, z)
    if whatT != None and whatT != 'g' and whatT != 'a' and whatT != 'w': 
      bte.visible  = True
      
      break
    else:
      bte.visible = False
def mine( terrainDic, vertexDic, subsets, _texture):
  if not bte.visible: 
    return
  else: 
    # - 0.5 on y
    wv = parseDict.getDictionary(vertexDic, floor(bte.x), floor(bte.y ), floor(bte.z))
    # have we got a block highlighted? if not return 
    if wv == None: return
    # mining is happening
    
    #(25, 215) wv - subset, subcube?
    for v in range(wv[1] +1, wv[1] + 37):
      # for the spot in this subset for each of the verticies ++ 999 to pos y
      subsets[wv[0]].model.vertices[v][1] += 999
    # Drop Collectable
    blockType = terrainDic.get((floor(bte.x), floor(bte.y), floor(bte.z)))
    drop_collectible(blockType, bte.position, _texture )
    
    subsets[wv[0]].model.generate()
    #Fall through floor
    # -0.5 on y
    # you could just floor once if you floored after passing through to the parse
    parseDict.recDictionary(terrainDic, floor(bte.x), floor(bte.y ), floor(bte.z), 'g')
    parseDict.recDictionary(vertexDic, floor(bte.x), floor(bte.y), floor(bte.z), None)
    # model is .5 off of the ursina model, the subset
    # + Vec3(0, -0.5, 0)
    return (bte.position , wv[0])
    
    
  
        
      