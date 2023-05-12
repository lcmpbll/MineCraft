from ursina import *
import random as rando
from config import *
import numpy as np

hotBarModel=load_model('quad',use_deepcopy=True)
hotbar = Entity(model=hotBarModel, parent=camera.ui)
# set size and position
hotbar.scale=Vec3(0.68,0.08,0)
# render me first
hotbar.render_queue = 0
# set appearance

hotbar.y=(-0.45 + (hotbar.scale_y*0.5))
hotbar.color = color.dark_gray

# Inventory main panel
iPanModel=load_model('quad',use_deepcopy=True)
iPan = Entity(model=iPanModel, parent=camera.ui)
# set size and position
iPan.rows = 3
iPan.scale_x=hotbar.scale_x
iPan.scale_y = hotbar.scale_y * iPan.rows
iPan.basePosY = hotbar.y + hotbar.scale_y * 2
iPan.gap = hotbar.scale_y
iPan.y = iPan.basePosY + iPan.gap
# render me on bottom
iPan.render_queue = 0
# set appearance
# ui_cols=hotbar.scale[0]/9
# iPan.y=hotbar.y + 
iPan.color = color.light_gray
iPan.visible = False

# moved up so they can be referred to in the static method
hotspots = []
items = []

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
    # this.onIPan = False
    this.visible= False
    this.occupied = False
    # render me second
    this.render_queue = 1
    #What item are we hosting 
    this.item = None
  @staticmethod
  def toggle(): #not a member function, doesn't apply to each item
    if iPan.visible:
      iPan.visible = False
    else:
      iPan.visible = True
    for h in hotspots:
      # game mode - not visisble, inventory - can see
      if not h.visible and not h.onHotbar:
        h.visible = True
        if h.item:
         h.item.visible = True
      elif not h.onHotbar: 
        # game mode
        h.visible = False
        if h.item:
          h.item.visible = False
          # disable item ?
       

class Item(Draggable):
  def __init__(this):
    super().__init__()
    this.model=load_model('quad',use_deepcopy=True)
    this.color=color.white
    this.scale_x = Hotspot.scalar*0.9
    # do me third
    this.render_queue = 2
    this.scale_y =  this.scale_x
    this.visible=False
    this.onHotBar=False
    # this.onIpan = False
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
  
  def fixPos(this, setUp = False):
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
      closestHotty.item = this
      # update previous hotspot's status
      if this.currentSpot:
        this.currentSpot.occupied = False
        this.currentSpot.item = None
      # finally update current hotspot
      this.currentSpot = closestHotty
      this.onHotBar = True
      
      
    elif this.currentSpot:
      #no hot spot available, just move back
      this.position = this.currentSpot.position
    # If found copy hot spots position
    
    # Set previous hot spot host to unoccupied
    # download items block type ect into host hot spot -- maybe just id
    # no unoccupied hotspot? ? return to current host position
      
       
  def drop(this):
    this.fixPos()
  

#Hotspots for the hot bar
for i in range(Hotspot.rowFit):
  bud = Hotspot()
  bud.onHotbar = True
  bud.visible = True
  padding = (hotbar.scale_x - bud.scale_x * Hotspot.rowFit) * 0.5
  bud.y = hotbar.y
  bud.x = (hotbar.x - hotbar.scale_x * 0.5 + Hotspot.scalar * 0.5 + padding + bud.scale_x * i)
  
  hotspots.append(bud)
  # HotSpots for Main Inventory panel
iPanSlots = []
items = []
#Hotspots for the hot bar, 
for j in range(iPan.rows):
  for i in range(Hotspot.rowFit):
    bud = Hotspot()
    bud.visible = False
    y_padding = (iPan.scale_x - Hotspot.scalar * iPan.rows) * 0.5 
    x_padding = (iPan.scale_x - Hotspot.scalar * Hotspot.rowFit) * 0.5
    # bud.y = iPan.y  +  (iPan.scale_y/iPan.rows * (j -1))  # is this because pos_y is not the bottom but the mid
    bud.y = (iPan.y + iPan.scale_y * 0.5 + Hotspot.scalar * 0.5 - y_padding + Hotspot.scalar * j)
    bud.x = (iPan.x - iPan.scale_x * 0.5 + Hotspot.scalar * 0.5 + x_padding + bud.scale_x * i)
  
  iPanSlots.append(bud)
# main inventory Items
for i in range(8):
  bud = Item()
  # bud.onHotBar= True
  bud.visible= True
  bud.x = rando.random() -0.5
  bud.y = rando.random() - 0.5
  setUp = True
  bud.fixPos(setUp)
  items.append(bud)  
  
def resetHotSpots(): 
  for h in hotspots:
    h.color = color.white
    
def inv_input(key, subject, mouse):
  try:
    wnum = int(key) -1
    
    if wnum >= 0 and wnum < 10:
      #make sure no hotspots are highlighted
      for h in hotspots:
        h.color = color.white
      resetHotSpots()
      hotspots[wnum].color = color.black
      if hotspots[wnum].occupied:
        subject.blockType = hotspots[wnum].item.blockType
        print(subject.blockType)
      
  except:
    pass
  if key == 'e' and subject.enabled:
    # in inventory mode
    Hotspot.toggle()
    subject.disable()
    mouse.locked = False
  elif key == 'e' and not subject.enabled:
    # game play mode
    Hotspot.toggle()
    mouse.locked = True
    subject.enable() 


