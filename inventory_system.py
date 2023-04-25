from ursina import *
import random as rando
from config import *
import numpy as np

hotBarModel=load_model('quad',use_deepcopy=True)
hotbar = Entity(model=hotBarModel, parent=camera.ui)
# set size and position
# hotbar.scale_y = 0.08
# hotbar.scale_x = 0.68
# set appearance
hotbar.scale=Vec3(0.68,0.08,0)
hotbar.position.y = -0.45 + (hotbar.scale_y * 0.5)
# ui_cols=hotbar.scale[0]/9
hotbar.y=(-0.45 + (hotbar.scale_y*0.5))
hotbar.color = color.dark_gray

class Hotspot(Entity):
  # Fix sides of hotspot to height of hot bar
  scalar=hotbar.scale_y*0.9
  # how many hot spots fit across the hot bar
  rowFit = 9
  def __init__(this):
    super().__init__()
    this.model='quad'
    this.parent=camera.ui
    this.scale_y=Hotspot.scalar
    this.scale_x = this.scale_y
    this.color=color.white
    this.texture='white_box'
    this.onHotbar = False
    this.visible=False
    this.occupied = False
    #What item are we hosting 
    this.item = None

class Item(Draggable):
  def __init__(this):
    super().__init__()
    this.model=load_model('quad',use_deepcopy=True)
    this.color=color.white
    this.scale_x = Hotspot.scalar*0.9
    this.scale_y =  this.scale_x
    this.visible=False
    this.onHotBar=False
    this.texture ='texture_atlas_3'
    this.texture_scale *= 64/this.texture.width
    this.blockType = mins[rando.randint(0,len(mins) -1)]
    this.currentSpot = None
    this.setTexture()
    this.setColor()
  def setTexture(this):
    uu = minerals[this.blockType][0]
    uv = minerals[this.blockType][1]
    basemod=load_model('block.obj',use_deepcopy=True)
    e=Empty(model=basemod)
    cb=copy(e.model.uvs)
    del cb[:-33]
    this.model.uvs = [Vec2(uu, uv) + u for u in cb]
    this.model.generate()
    this.rotation_z = 180
  
  def setColor(this):
    if len(minerals[this.blockType]) > 2:
      this.color = minerals[this.blockType][2]
  
  def fixPos(this):
    closest = -1
    closestHotty = None
    # Look through hotspots, 
    for h in hotspots:
    # Find unoccupied hotspot that is closest
      if h.occupied: continue
      dist = h.position - this.position
      # get magnitude of dist
      dist = np.linalg.norm(dist)
      if dist < closest or closest == -1:
        # we have a new closest
        closest = dist
        closestHotty = h
      #found a unoccupied hotspot
    if closestHotty != None:
      #update new host with item information
      closestHotty.occupied = True
      this.position = closestHotty.position
      # update previous hotspot's status
      if this.currentSpot:
        this.currentSpot.occupied = False
        this.currentSpot.item = None
      # finally update current hotspot
      this.currentSpot = closestHotty
      
      
    elif this.currentSpot:
      #no hot spot available, just move back
      this.position = this.currentSpot.position
    # If found copy hot spots position
    
    # Set previous hot spot host to unoccupied
    # download items block type ect into host hot spot -- maybe just id
    # no unoccupied hotspot? ? return to current host position
      
       
  def drop(this):
    this.fixPos()
  
hotspots = []
items = []
#Hotspots for the hot bar
for i in range(Hotspot.rowFit):
  bud = Hotspot()
  bud.onHotbar=True
  bud.visible = True
  padding = (hotbar.scale_x - bud.scale_x * Hotspot.rowFit) * 0.5
  bud.y = hotbar.y
  bud.x = (hotbar.x - hotbar.scale_x * 0.5 + bud.scale_x * 0.5 + padding + bud.scale_x * i)
  
  hotspots.append(bud)

for i in range(99):
  bud = Item()
  bud.onHotBar=True
  bud.visible=True
  bud.x = rando.random() -0.5
  bud.y = rando.random() - 0.5
  items.append(bud)  
  
    
def inv_input(key, subject, mouse):
  if key == 'e' and subject.enabled:
    subject.disable()
    mouse.locked = False
  elif key == 'e' and not subject.enabled:
    mouse.locked = True
    subject.enable() 


