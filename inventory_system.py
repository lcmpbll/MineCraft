from ursina import *
import random as rando
from config import *
import numpy as np


hotBarModel=load_model('quad',use_deepcopy=True)
hotbar = Entity(model=hotBarModel, parent=camera.ui)
# set size and position
hotbar.scale=Vec3(0.68,0.08,0)
# render me on the bottom
# hotbar.render_queue = 0
hotbar.z = 0
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
# iPan.render_queue = 0
iPan.z = 0
# set appearance
# ui_cols=hotbar.scale[0]/9
# iPan.y=hotbar.y + 
iPan.color = color.light_gray
iPan.visible = False

# moved up so they can be referred to in the static method
hotspots = []
#iPanSlots = []
items = []

class Hotspot(Entity):
  # Fix sides of hotspot to height of hot bar
  scalar=hotbar.scale_y*0.9
  # how many hot spots fit across the hot bar
  rowFit = 9
  def __init__(this):
    super().__init__()
    this.model=load_model('quad', use_deepcopy=True)
    this.parent=camera.ui
    this.scale_y=Hotspot.scalar
    this.scale_x = this.scale_y
    this.color=color.white
    this.texture='white_box'
    this.onHotbar = False
    this.visible= False
    this.occupied = False
    this.selected = False
    # render me second
    # this.render_queue = 1
    this.z = -1
    #What item are we hosting 
    this.item = None
    # new stack system
    # start with no items as default
    this.stack = 0
    this.fullStack = 64
    # text 
    this.t = Text("", scale=1)
    
  @ staticmethod 
  def check_hotBar(hotspot):
    if hotspot.onHotbar:
      return True
    return False
  @staticmethod
  def toggle(): #not a member function, doesn't apply to each item
    if iPan.visible:
      iPan.visible = False
    else:
      iPan.visible = True

    for h in hotspots:
  
      # game mode - not visisble, inventory - can see
      if h.visible == False and h.onHotbar == False:
        h.visible = True
        if h.item:
         h.item.visible = True
         h.visible = True
         h.t.visible = True
      elif not h.onHotbar: 
        # game mode
        h.visible = False
        if h.item:
          h.item.visible = False
          h.t.visible = False
          # disable item ?
       

class Item(Draggable):
  def __init__(this, blockType=mins[rando.randint(0,len(mins) -1)]):
    super().__init__()
    this.model=load_model('quad',use_deepcopy=True)
    this.color=color.white
    this.scale_x = Hotspot.scalar*0.9
    # do me third
    # this.render_queue = 2
    this.z = -2
    this.scale_y =  this.scale_x
    this.visible=False
    this.onHotbar=False
    # this.onIpan = False
    this.texture ='texture_atlas_3'
    this.texture_scale *= 64/this.texture.width
    this.blockType = blockType
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
    # Find unoccupied hotspot that is closest and not on the iPan during setup
      if setUp == True and not h.onHotbar: continue
      # if it is not set up you can add to occupied stacks
      if setUp == False: 
        # if the stack is occupied
        if h.occupied == True:
          # make sure it is the same block type and the stack is not full
          if this.blockType != h.item.blockType: continue
          elif h.item.blockType == this.blockType and h.stack < h.fullStack:
              closestHotty = h
              break
          # if it is an unoccupied stack feel free to place it there
          elif h.occupied == False:
            closestHotty = h
      # when setting up use a unoccupied stack
      elif h.occupied == False:
        closestHotty = h
        break
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
      # update previous hotspot's status, if switching spots
      transferStack = 0
      if setUp == False and this.currentSpot.stack != 0:
        # remove item data from prev hotspot
        this.currentSpot.occupied = False
        this.currentSpot.item = None
        transferStack = this.currentSpot.stack
        this.currentSpot.stack = 0
        this.currentSpot.t.text = "  "
      # finally update current hotspot
      this.currentSpot = closestHotty
      this.visible = closestHotty.visible
      # set visibility
      if closestHotty.onHotbar == True:
        this.onHotbar = True
      else: 
        this.onHotbar = False
      if transferStack == 0:
        this.currentSpot.stack += 1
      elif this.currentSpot.stack == 0:
        this.currentSpot.stack += transferStack
        
      else:
        this.currentSpot.stack += transferStack
        destroy(this)
        
      # this.currentSpot.t.text = "<white><bold>"+ str(this.currentSpot.stack)
      
      
    elif this.currentSpot:
      #no hot spot available, just move back
      this.position = this.currentSpot.position
    # If found copy hot spots position
    
    # Set previous hot spot host to unoccupied
    # download items block type ect into host hot spot -- maybe just id
    # no unoccupied hotspot? ? return to current host position
      
  def update_stack_text(this):
    stackNum = this.currentSpot.stack
    myText = "<white><bold>" + str(stackNum)
    this.currentSpot.t.text = myText 
    # not sure why, but displaces hotspots when active. 
    # this.currentSpot.origin = (-0.75,-0.55)
    # this.currentSpot.t.z = -3
    # this.currentSpot.t.x = this.currentSpot.x
    # this.currentSpot.t.y = this.currentSpot.y    
  def drop(this):
    if this.visible == False:
      return
    this.fixPos()
    this.update_stack_text()
    
    # display blocks in this hotspots stack 
    # Hotspot.checkStackNum(this.currentSpot)
    
  
  @staticmethod
  def spot_check(_blockType):
    
    foundSpot = False
    for h in hotspots:
      if not h.onHotbar: continue
      if h.occupied:
        if h.item.blockType == _blockType and h.stack < h.fullStack:
          h.stack += 1
          h.item.update_stack_text()
          foundSpot = True 
          break
      else: continue
    if foundSpot == False:
      for h in hotspots:
        if not h.onHotbar: continue
        if not h.occupied:
          item = Item(_blockType)
          setUp = True
          item.fixPos(setUp)
          item.update_stack_text()
          foundSpot = True
          break
    return foundSpot
  
  @staticmethod
  def new_item(_blockType):
    #First check if there is already this stack on the hot bar?
    # if yes increment hotbar stack, this would prevent stacks from being physical
    # if no and space available increment that stack
    # we are not currently using the items list
    aStack = Item.spot_check(_blockType)
    if aStack == True:
      
      return True
    else: return False
      
    # 
    # newI = Item(_blockType)
    # setUp = True
    # Item.fixPos(newI, setUp)

#Hotspots for the hot bar
for i in range(Hotspot.rowFit):
  bud = Hotspot()
  bud.onHotbar = True
  bud.visible = True
  padding = (hotbar.scale_x - bud.scale_x * Hotspot.rowFit) * 0.5
  bud.y = hotbar.y
  bud.x = (hotbar.x - hotbar.scale_x * 0.5 + Hotspot.scalar * 0.5 * 1.1 + bud.scale_x * i * 1.07)
  bud.t.origin = (-0.75,-0.55)
  bud.t.z = -3
  bud.t.x = bud.x
  bud.t.y = bud.y
  
  hotspots.append(bud)
  # HotSpots for Main Inventory panel

#Hotspots for the hot bar, 

for j in range(iPan.rows):
  for i in range(Hotspot.rowFit):
    bud = Hotspot()
    bud.onHotbar = False
    bud.visible = False
    y_padding = (iPan.scale_x - Hotspot.scalar * iPan.rows) * 0.5 
    x_padding = (iPan.scale_x - Hotspot.scalar * Hotspot.rowFit) * 0.5
    # bud.y = iPan.y  +  (iPan.scale_y/iPan.rows * (j -1))  # is this because pos_y is not the bottom but the mid
    bud.y = (iPan.y - iPan.scale_y * 0.5 + Hotspot.scalar * 0.5 * 1.1 + Hotspot.scalar * j * 1.11)
    bud.x = (iPan.x - iPan.scale_x * 0.5 + Hotspot.scalar * 0.5 * 1.05 + bud.scale_x * i * 1.05)
    bud.t.origin = (-0.75,-0.55)
    bud.t.z = -3
    bud.t.x = bud.x
    bud.t.y = bud.y
    bud.t.visible = bud.visible
    hotspots.append(bud)

# main inventory Items
# for i in range(8):
#   bud = Item()
#   # bud.onHotbar= True
#   bud.visible= True
#   bud.x = rando.random() -0.5
#   bud.y = rando.random() - 0.5
#   setUp = True
#   bud.fixPos(setUp)
#   items.append(bud)  
  
# make sure non hotbar items are invisible at the start
# my module does not start with items on the iPan
Hotspot.toggle()
Hotspot.toggle()
  
def resetHotSpots(): 
  for h in hotspots:
    h.color = color.white
    h.selected = False
    
wai = Text("<bold><pink>" + 'Nowhere', scale = 1.4, position=(-.75, 0.5))
   
def inv_input(key, subject, mouse):
  wai.text  = f'<bold><pink> East:{floor(subject.x)}, North:{floor(subject.z)}, Elevation: {floor(subject.y)}'
  try:
    wnum = int(key) -1
    
    if wnum >= 0 and wnum < 10:
      #make sure no hotspots are highlighted
      for h in hotspots:
        h.color = color.white
      resetHotSpots()
      hotspots[wnum].color = color.black
      hotspots[wnum].selected = True
      if hotspots[wnum].occupied:
        subject.blockType = hotspots[wnum].item.blockType
      else:
        subject.blockType = None
      
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


