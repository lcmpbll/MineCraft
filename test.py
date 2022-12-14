from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from numpy import floor
from numpy import abs
from numpy import sin
from numpy import cos
from random import randrange
from numpy import radians
import time
from perlin_noise import PerlinNoise
from nMap import nMap

app = Ursina()
prevTime = time.time()
 #window
window.color = color.rgb(0, 200, 211)
window.exit_button.visible = False
window.fullscreen = False
scene.fog_color = color.rgb( 0, 222, 0 )
scene.fog_density = 0.10
# Texture make lighter on the outside
grassStrokeTex = load_texture('grass.png')
#wireTex = load_texture('wireframe.png)
#storeText = load_textuure('grass_mono.png)
bte = Entity(model='cube') 
              #texture=wireTex)
class BTYPE:
  STONE = color.rgb(255, 255, 255)
  GRASS = color.rgb(0, 255, 0) 
  SOIL = color.rgb(255, 80, 100)
  RUBY = color.rgb(255, 0, 0)
        
            
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
  global prevX, prevZ, prevTime, genSpeed, perCycle, origin, rad, generating, canGenerate
  if abs(subject.z - prevZ) > 1 or abs(subject.x - prevX) > 1:
    origin = subject.position
    rad = 0
    prevZ = subject.z
    prevX = subject.x
    generating = 1 * canGenerate
    
    generateShell()
  if time.time() - prevTime > genSpeed :
    for i in range(perCycle):
      genTerrain()
    prevTime = time.time()
    
  vincent.look_at(subject, 'forward')
  #vincent.rotation_x = 0 <- prevents vincent from leaning forward
  buildTool()
    
 # terrain  
 #subcubes make up subsets and subsets make up terrain

# terrainWidth = 40
# subWidth = int(terrainWidth/10)
subsets = []
subCubes = []

# Perlin Noise
noise = PerlinNoise(octaves=1, seed=99)

# New Terrain variables

genSpeed = 0
perCycle = 16
currentCube = 0
numSubCubes = 16
theta = 0
rad = 0
currentSubset = 0
numSubsets = 420
radLimit = 128

# a dictionary for recording wether terrain exist at location specified in key
subDic = {}


#Instantiate ghost subset cubes
for i in range(numSubCubes):
  bud = Entity(model='cube')
  bud.disable()
  subCubes.append(bud)
   
# Instantiate empty Subsets
for i in range(numSubsets):
  bud = Entity(model=None) 
  bud.texture = grassStrokeTex
  bud.disable()
  subsets.append(bud)
  
# making y for positions
def genPerlin(_x, _z):
  y = 0
  freq = 64
  amp = 42
  y+= ((noise([_x/freq, _z/freq]))*amp)
  ## octaves
  freq = 32
  amp = 21
  y += ((noise([_x/freq, _z/freq]))*amp)
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
    subCubes[currentCube].y = genPerlin(x,z)
    subCubes[currentCube].disable()
    currentCube += 1
    if currentCube == numSubCubes:
      subsets[currentSubset].combine(auto_destroy=False)
      subsets[currentSubset].enable()
      currentSubset += 1
      currentCube = 0
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
  global shellWidth, amp, freq
  for i in range(len(shellies)):
    x = shellies[i].x = floor((i/shellWidth) + subject.x - 0.5 * shellWidth)
    z = shellies[i].z = floor((i%shellWidth) + subject.z - 0.5 * shellWidth)
    shellies[i].y = genPerlin(x,z)
   
   
 
subject = FirstPersonController()
subject.cursor.visible = False
subject.gravity = .5
# can set two variables at the same time
subject.x = subject.z = 5
subject.y = 64
prevZ = subject.Z
prevX = subject.x
origin = subject.position #Vec 3 objet, .x, .y, .z

chickenModel = load_model('cube')
vincent = Entity(model=chickenModel, scale = 9,
                  x = 22, z = 16, y = 4,
                  color = (color.red),
                  double_sided=True)

generateShell()
  
app.run()