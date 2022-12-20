from ursina import *
# Petter Amland
from ursina.prefabs.first_person_controller import FirstPersonController
from numpy import floor, abs, sin, cos, radians
# from random import randrange
import time
from perlin_noise import PerlinNoise
from nMap import nMap

app = Ursina()
prevTime = time.time()
 #window
window.color = color.rgb(0, 200, 211)
window.exit_button.visible = False
window.fullscreen = False
# scene.fog_color = color.rgb( 0, 222, 0 )
# scene.fog_density = 0.10
# Texture make lighter on the outside
grassStrokeTex = 'grass_mono.png'
wireTex = 'wireframe.png'
stoneTex = 'block_texture.png'
chickenTex = 'chicken.png'
cubeTex = 'block_texture.png'
cubeModel = 'block.obj'
wireTex = 'wireframe.png'
storeText = 'grass_mono.png'
axoTex= 'axoltl.png'
axoModel = 'axolotl.obj'

bte = Entity(model='cube', texture=wireTex)
class BTYPE:
  STONE = color.rgb(255, 255, 255)
  GRASS = color.rgb(0, 255, 0) 
  SOIL = color.rgb(255, 80, 100)
  RUBY = color.rgb(255, 0, 0)    
#block type default 
     
blockType = BTYPE.SOIL
buildMode = -1 # -1 is off 1 is on
 # terrain generation control
 # # 1 is on -1 is off  
  
canGenerate = 1 
generating = 1   
## I think this isn't workin yet because of texture.

def buildTool(): 
  if buildMode == -1:
    bte.visible = False
    return
  else: bte.visible = True
  
  bte.position = round(subject.position + camera.forward * 3)
  bte.y += 2
  bte.y = round(bte.y)
  bte.x = round(bte.x)
  bte.z = round(bte.z)
  bte.color = blockType
  
 
def build():
  e = duplicate(bte)
  e.collider = 'cube'
  e.texture = grassStrokeTex
  e.color = blockType
  e.shake(duration=0.5, speed=0.01)
  #stone text
  
  
def input(key):
  global blockType, buildMode, generating, canGenerate
  if key == 'q' or key == 'escape':
    quit()
  if key == 'g':
    generating *= -1
    canGenerate *= -1
  if buildMode == 1:
    if key == 'left mouse up': 
        build()
    elif key == 'right mouse up':  ##else if
      e = mouse.hovered_entity
      destroy(e)
  if key == 'f': buildMode *= -1
  if key == '1': blockType = BTYPE.SOIL
  if key == '2': blockType = BTYPE.GRASS
  if key == '3': blockType = BTYPE.STONE
  if key == '4': blockType = BTYPE.RUBY
  
 
def update():
  global prevX, prevZ, prevTime, genSpeed, perCycle, origin, rad, generating, canGenerate, theta, subject
  if abs(subject.z - prevZ) > 1 or abs(subject.x - prevX) > 1:
    origin = subject.position
    rad = 0
    theta = 0
    prevZ = subject.z
    prevX = subject.x
    generating = 1 * canGenerate
    generateShell()
  if time.time() - prevTime > genSpeed :
    for i in range(perCycle):
      genTerrain()
    prevTime = time.time()
  # if subject.y < - genPerlin(subject.x, subject.y) - 100:  #safety net sets user back at a height of subject height incase of glitching through terrain
  #   subject.y = subject.height + genPerlin(subject.x, subject.y) + 2
  #   subject.land() 
  vincent.look_at(subject, 'forward')
  #vincent.rotation_x = 0 <- prevents vincent from leaning forward
  buildTool()
    
 # terrain  
 #subcubes make up subsets and subsets make up terrain

# terrainWidth = 40
# subWidth = int(terrainWidth/10)
megasets = []
subsets = []
subCubes = []

# Perlin Noise
noise = PerlinNoise(octaves=1, seed=99)

# New Terrain variables
genSpeed = 0
#generate terrain called 16 times update perloop
perCycle = 64
currentCube = 0
numSubCubes = 64
theta = 0
rad = 0
currentSubset = 0
# how many combine in to a megaset
numSubsets = 420
radLimit = 128
# a dictionary for recording wether terrain exist at location specified in key
subDic = {}
caveDic = { 'x9z9': 'cave', 'x10z9': 'cave', 'x11z9': 'cave', 'x12z9': 'cave'  }

#Instantiate ghost subset cubes
for i in range(numSubCubes):
  #switching to cubeModel is not great.
  bud = Entity(model=cubeModel, texture=cubeTex)
  bud.rotation_y = random.randint(0, 4) * 90
  bud.disable()
  subCubes.append(bud)
   
# Instantiate empty Subsets
for i in range(numSubsets):
  bud = Entity(model=cubeModel) 
  bud.texture = cubeTex
  bud.disable()
  subsets.append(bud)
  
# making y for positions
def genPerlin(_x, _z):
  global caveDic
  y = 0
  freq = 64
  amp = 42
  y+= ((noise([_x/freq, _z/freq]))*amp)
  ## octaves
  freq = 32
  amp = 21
  y += ((noise([_x/freq, _z/freq]))*amp)
  if caveDic.get('x' + str(int(_x)) + 'z' + str(int(_z))) == 'cave':
    y += -32
  return floor(y)



def genTerrain():
  global currentCube, theta, rad, origin, currentSubset, generating
  #Where the new terrain starts
  if generating == -1: return 
  x = floor(origin.x + sin(radians(theta)) * rad)
  z = floor(origin.z + cos(radians(theta)) * rad)
  #Checks wether there is terrain there already
  if subDic.get('x'+ str(x) + 'z' + str(z)) != 'i':
    subCubes[currentCube].enable()
    subCubes[currentCube].x = x
    subCubes[currentCube].z = z
    subDic['x'+ str(x) + 'z' + str(z)] = 'i'
    subCubes[currentCube].parent = subsets[currentSubset]
    y = subCubes[currentCube].y = genPerlin(x,z)
    #nMap takes the y position and will take a 21? returns a number between 112 243
    c = nMap(y, -8, 21, 132, 223)
    c += random.randint(-32, 32)
    subCubes[currentCube].color = color.rgb(c, c, c)
    subCubes[currentCube].disable()
    currentCube += 1
    
    # Ready to form a subset?
    if currentCube == numSubCubes:
      subsets[currentSubset].combine(auto_destroy=False)
      subsets[currentSubset].enable()
      currentSubset += 1
      currentCube = 0
      # Ready to build a megaset? 
      # [-1] last thing in list
      if currentSubset == numSubsets:
        megasets.append(Entity(model=cubeModel, texture=cubeTex))
        # parent all subsets to new megaset
        for s in subsets:
          s.parent = megasets[-1]
        megasets[-1].combine(auto_destroy = False)
        currentSubset = 0
        print("megaset # " + str(len(megasets)))
        
  else:
    pass   
  #there was terrain already there so continue rotaation to find new terrain spot
  if rad > 0:
    theta += 45/rad
  else: 
    rad += 1 
  if theta >= 360:
    theta = 0
    rad += .5
    
  
  

  #below collider for 6 * 6 area
shellies = []
shellWidth = 3
for i in range(shellWidth * shellWidth): 
  bud = Entity(model='cube', collider='box')
  bud.visible = False
  shellies.append(bud)

def generateShell():
  # new gravity system for moving the subject
  global subject
  target_y = genPerlin(subject.x, subject.z) + 2
  if target_y - subject.y > 1: #cant step up that far
    pass
  else:
    subject.y = lerp(subject.y, target_y, 9.807 * time.dt)
  #lerp goes from one number to another in a controlled way, by time.dt multiply to standardize for different performance
  # global shellWidth
  # for i in range(len(shellies)):
  #   x = shellies[i].x = floor((i/shellWidth) + subject.x - 0.5 * shellWidth)
  #   z = shellies[i].z = floor((i%shellWidth) + subject.z - 0.5 * shellWidth)
  #   shellies[i].y = genPerlin(x,z)
   
   
 
subject = FirstPersonController()
subject.cursor.visible = False
subject.gravity = 0
# subject.height = 2
# can set two variables at the same time
subject.x = subject.z = 5
subject.y = 32
prevZ = subject.Z
prevX = subject.x
origin = subject.position #Vec 3 objet, .x, .y, .z

chickenModel = load_model('chicken.obj')
vincent = Entity(model=chickenModel, scale = 2,
                  texture=chickenTex,
                  x = 22, z = 16, y = 4 ,
                  # color = (color.red),
                  double_sided=True)
                  

# baby = Entity(model=axoModel, scale = 2,
#                   texture=axoTex,
#                   x = 13, z = 12, y = 4 ,
#                   # color = (color.red),
#                   double_sided=True)

generateShell()
  
app.run()