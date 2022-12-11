from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from numpy import floor
from numpy import abs
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

def input(key):
  if key == 'q' or key == 'escape':
    quit()
  if key == 'g':
    generateSubset()
 
def update():
  global prevX, prevZ, prevTime
  if abs(subject.z - prevZ) > 1 or abs(subject.x - prevX) > 1:
    generateShell() 
  if time.time() - prevTime > 0.004 :
    generateSubset()
    prevTime = time.time()
  if subject.y < -amp + 1:  #safety net sets user back at a height of subject height incase of glitching through terrain
    subject.y = subject.height + floor((noise([subject.x/freq,subject.z/freq]))*amp) 
    subject.land()
  vincent.look_at(subject, 'forward')
  #vincent.rotation_x = 0 <- prevents vincent from leaning forward
    
 # terrain  
 #subcubes make up subsets and subsets make up terrain
terrain = Entity(model=None, collider=None)
terrainWidth = 20
subWidth = int(terrainWidth/10)
subsets = []
subCubes = []
sci = 0 # subcubeindex
currentSubset = 0
# Perlin Noise
noise = PerlinNoise(octaves=4, seed=99)
amp = 24
freq = 100

#Instanciate ghost subset cubes
for i in range(subWidth):
  bud = Entity(model='cube')
  subCubes.append(bud)
  
# Instantiate empty Subsets
for i in range(int((terrainWidth * terrainWidth)/subWidth)):
  bud = Entity(model=None) 
  subsets.append(bud)

def generateSubset():
  global currentSubset, sci, amp, freq
  if currentSubset >= len(subsets): return
  for i in range(subWidth): 
    x = subCubes[i].x = floor((i + sci)/terrainWidth)
    z = subCubes[i].z = floor((i + sci)%terrainWidth)
    y = subCubes[i].y = floor((noise([x/freq,z/freq]))*amp)
    subCubes[i].parent = subsets[currentSubset]
    #Set color of subcube
    r = 0 
    g = 0 
    b = 0
    if y > amp* 0.03: 
      b = 255
    if y == 4: 
      r=g=b=255
    else:
      g = nMap(y, 0, amp*.5, 0, 255)
    subCubes[i].color = color.rgb(r,g,b)
    subCubes[i].visible = False
    
  subsets[currentSubset].combine(auto_destroy = False)
  subsets[currentSubset].texture = grassStrokeTex
  sci += subWidth
  currentSubset += 1 
  
  terrainFinished = False 
  def finishTerrain():
    if terrainFinished == True : return
    terrain.texture = grassStrokeTex
    terrain.combine()
    terrainFinished = True
    
    
             

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
    shellies[i].y = floor((noise([x/freq, z/freq]))*amp)
   
   
 
subject = FirstPersonController()
subject.cursor.visible = False
subject.gravity = .5
# can set two variables at the same time
subject.x = subject.z = 5
subject.y = 12
prevZ = subject.Z
prevX = subject.x

chickenModel = load_model('cube')
vincent = Entity(model=chickenModel, scale = 3,
                  x = 22, z = 16, y = 4,
                  color = (color.red),
                  double_sided=True)

generateShell()
  
app.run()
