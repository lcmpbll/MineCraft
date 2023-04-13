from ursina import Entity, color, floor, Vec3
from dictionary_craft import DictionaryCraft
# class MiningSystem:
#     def __init__(this): not a class ?
# this lots of red and green make yellow, 0.4 makes it shiny
bte = Entity(model='cube', color=color.rgba(1,1,0,0.4))
bte.scale = 1.001
parseDict = DictionaryCraft()
def highlight( pos, camera, terrainDic):
  # some times I fall through the terrain after building
  for i in range(30, 1, -1):
    #adjust for player's height
    wp = pos + Vec3(0, 1.86, 0) + camera.forward * (i * 0.5)
    #round to improve accuracy,  can still be improved
    x = round(wp.x)
    y = floor(wp.y)
    z = round(wp.z)
    bte.y = y + 0.5
    bte.z = z
    bte.x = x
    if parseDict.getDictionary(terrainDic, x, y, z) == 't': 
      bte.visible  = True
      
      break
    else:
      bte.visible = False
def mine( terrainDic, vertexDic, subsets):
  if not bte.visible: 
    return
  else: 
    wv = parseDict.getDictionary(vertexDic, floor(bte.x), floor(bte.y - 0.5), floor(bte.z))
    # have we got a block highlighted? if not return 
    if wv == None: return
    #(25, 215) wv - subset, subcube?
    for v in range(wv[1] +1, wv[1] + 37):
      # for the spot in this subset for each of the verticies ++ 999 to pos y
      subsets[wv[0]].model.vertices[v][1] += 999
    subsets[wv[0]].model.generate()
    #Fall through floor
    # you could just floor once if you floored after passing through to the parse
    parseDict.recDictionary(terrainDic, floor(bte.x), floor(bte.y - 0.5), floor(bte.z), 'g')
    parseDict.recDictionary(vertexDic, floor(bte.x), floor(bte.y -0.5), floor(bte.z), None)
    # model is .5 off of the ursina model, the subset
    return (bte.position + Vec3(0, -0.5, 0), wv[0])
    
    
  
        
      