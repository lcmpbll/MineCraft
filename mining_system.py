from ursina import Entity, color, floor
from dictionary_craft import DictionaryCraft
class MiningSystem:
    def __init__(this):
      # this lots of red and green make yellow, 0.4 makes it shiny
      this.bte = Entity(model='cube', color=color.rgba(1,1,0,0.4))
      this.bte.scale = 1.001
      this.parseDict = DictionaryCraft()
    def highlight(this, pos, camera, terrainDic):

      for i in range(15, 1, -1):
        wp = pos + camera.forward * i 
        print(wp)
        x = floor(wp.x)
        y = floor(wp.y + 3)
        z = floor(wp.z)
        this.bte.y = y + 0.5
        this.bte.z = z
        this.bte.x = x
        c = this.parseDict.getDictionary(terrainDic, x, y, z)
        if this.parseDict.getDictionary(terrainDic, x, y, z) == 't': 
          this.bte.visible  = True
          
          break
        else:
          this.bte.visible = False
        
      