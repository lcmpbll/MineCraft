from ursina import *
# Petter Amland
from ursina.prefabs.first_person_controller import FirstPersonController
from numpy import floor, abs, sin, cos, radians
from random import randrange
import time
from perlin_noise import PerlinNoise
from nMap import nMap
from cave_system import Caves
from tree_roots import Trees
from mining_system import Mining_system

app = Ursina()

## Textures 
chickenTex = 'chicken.png'
cubeTex = 'block_texture.png'
buildTex = 'build_texture.png'
cubeModel = 'moonCube.obj'
axoTex= 'b_axolotl.png'
axoModel = 'b_axolotl.obj'
axeModel = 'Diamond-Pickaxe.obj'
axeTex = 'Diamond_axe_tex.png'

# switch between 1, -1 to control terrain generation
canGenerate = 1 
generating = 1 

# terrain  
#subcubes make up subsets and subsets make up terrain
megasets = []
subsets = []
subCubes = []
# Perlin Noise
noise = PerlinNoise(octaves=1, seed=int(randrange(1,99)))
#Displays the seed number
seedMouth = Text( text='Your seed is ' + str(noise.seed), background=True)
seedMouth.background.color=color.rgba(0, 20, 100, 222)
seedMouth.scale *= 0.09
# seedMouth.x = -1
# seedMouth.y = 0.5
seedMouth.appear(speed = .15)

# New Terrain variables
genSpeed = 0
#generate terrain called 16 times update perloop
perCycle = 64
currentCube = 0
currentSubset = 0
currentMegaset = 0
theta = 0
rad = 0
# How many to combine into a subset
numSubCubes = 64
# how many combine in to a megaset
numSubsets = 420
# number of instanciated megasets
numMegasets = 99
radLimit = 128
# a dictionary for recording wether terrain exist at location specified in key
subDic = {}  

# Our main character
subject = FirstPersonController()
subject.cursor.visible = False
subject.gravity = 0
grav_speed = 0
grav_acc = 0.1
# subject.height = 2
# can set two variables at the same time
subject.x = subject.z = 5
subject.y = 0
prevZ = subject.Z
prevX = subject.x
origin = subject.position #Vec 3 objet, .x, .y, .z

# Our axe
axe = Entity(model=axeModel, scale=0.05, texture=axeTex, position=subject.position, always_on_top=True)
axe.x -= 3
axe.z -= 2.2
axe.y -= subject.y
axe.rotation_y = 90
axe.rotation_x = 90
axe.parent = camera

def resetTerrainVs():
  global currentCube, currentSubset, currentMegaset, theta
  global rad, generating, canGenerate, subject
  currentCube = 0
  currentSubset = 0
  currentMegaset = 1
  theta = 0
  rad = 0
  generating = -1
  canGenerate = -1
  subject.rotation = Vec3(0, 0, 0)
  
def createTerrainEntities():
  # global numMegasets
  # in terrain_system
  for i in range(numSubCubes):
    #switching to cubeModel is not great.
    bud = Entity(model=cubeModel, texture=cubeTex)
    bud.scale *= 0.99999
    bud.rotation_y = random.randint(0, 4) * 90
    bud.disable()
    subCubes.append(bud)
    
  # # Instantiate empty Subsets
  for i in range(numSubsets):
    bud = Entity(model=cubeModel) 
    bud.texture = cubeTex
    bud.disable()
    subsets.append(bud)
    
  #instantiate empty megasets
  for i in range(numMegasets):
    bud = Entity(model=cubeModel)
    bud.texture = cubeTex
    bud.scale *= 0.99999999
    bud.disable()
    megasets.append(bud)
    
createTerrainEntities()

# Save and load file functions :-D
def save():
  global subsets, megasets, subDic, noise
  import pickle, os, sys
  # Create a new entity that combines all current variables
  # ie subsets, megasets which we can place on to a file
  # first open/create file in the folder(working directory) that we can save to
  path = os.path.dirname(os.path.abspath(sys.argv[0]))
  os.chdir(path)
  with open('pickling.txt', 'wb') as f:
    e = Entity()
    for s in subsets:
      if s.enabled == True:
        s.parent = e
    for m in megasets:
      if m.enabled == True:
        m.parent = e
    e.combine(auto_destroy = False)
    # take individual parts that make up a mesh
    terrainModel = [  e.model.vertices,
                      e.model.triangles,
                      e.model.colors,
                      e.model.uvs  ]
    #reparent so they are not destroyed with e
    for s in subsets:
      s.parent = scene
    for m in megasets:
      m.parent = scene
    destroy(e)
    
    buildsModel = [ varch.builds.model.vertices,
                    varch.builds.model.triangles,
                    varch.builds.model.colors,
                    varch.builds.model.uvs  ]
    newlist = [ 
                subject.position,
                varch.tDic,
                subDic,
                terrainModel,
                noise,
                buildsModel
              ]
    # write game state object to file 
    # then clear out temporary lists
    pickle.dump(newlist, f)
    newlist.clear()
    terrainModel.clear()


   
      
    
    

def load():
  import pickle, os, sys
  global subDic, noise, currentSubset, currentCube, currentMegaset
  # Open main module directory of correct file
  path = os.path.dirname(os.path.abspath(sys.argv[0]))
  os.chdir(path)
  with open('pickling.txt', 'rb') as f:
    nd = pickle.load(f)
    # populate our familiar terrain variables with the saved data.
    subject.position = copy(nd[0])
    varch.tDic = copy(nd[1])
    subDic = copy(nd[2])
    terrainModel = copy(nd[3])
    noise = copy(nd[4])
    buildsModel = copy(nd[5])
    
    # Now delete current terrain and builds
    for s in subCubes:
      destroy(s)
    for s in subsets:
      destroy(s)
    for m in megasets:
      destroy(m)
    destroy(varch.builds)
    
    subCubes.clear()
    subsets.clear()
    megasets.clear()
    
    createTerrainEntities()

    
    megasets[0].enable()
    
    megasets[0] = Entity(model=Mesh(
                    vertices = terrainModel[0],
                    triangles = terrainModel[1],
                    colors = terrainModel[2],
                    uvs = terrainModel[3]
                  ), texture = cubeTex)
    # resest terrain Generation Varaibles
    varch.builds = Entity(model=Mesh(
        vertices = buildsModel[0],
        triangles = buildsModel[1],
        colors = buildsModel[2],
        uvs = buildsModel[3]
    ), texture = buildTex)
    
    resetTerrainVs()
    
      
  
  
#will create a cave system object called anush
anush = Caves()
solar = Trees()
varch = Mining_system(subject, axe, camera, subsets, megasets)
# bte = BuildToolEntity()
prevTime = time.time()
 #window
window.color = color.rgb(0, 200, 211)
window.exit_button.visible = False
window.fullscreen = False
# scene.fog_color = color.rgb( 0, 222, 0 )
# scene.fog_density = 0.10
      
def input(key):
  global generating, canGenerate, seedMouth
  if key == 'q' or key == 'escape':
    quit()
  #smooth building
  if varch.buildMode == 1:
    generating = -1
    canGenerate = -1
  if key == 'g':
    generating *= -1
    canGenerate *= -1
  if key == 'c':
    pass
    #seedMouth.destroy()
  if key == 'b':
    save()
  if key == 'o':
    load()
    
 
  else: 
    # generating = 1
    # canGenerate = 1
    varch.input(key)

  
# Main game loop
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
  vincent.rotation_x = 0 #<- prevents vincent from leaning forward
  #controls mining and building functions
  varch.buildTool()

# making y for positions
def genPerlin(_x, _z, plantTree=False):
  y = 0
  freq = 64
  amp = 42
  y+= ((noise([_x/freq, _z/freq]))*amp)
  ## octaves
  freq = 32
  amp = 21
  y += ((noise([_x/freq, _z/freq]))*amp)
  whatCaveHeight = anush.checkCave(_x, _z)
  if whatCaveHeight != None:
    y = anush.checkCave(_x, _z)
  elif plantTree == True : solar.checkTree(_x, floor(y), _z)
  
  return floor(y)

def genTerrain():
  global currentCube, theta, rad, origin, currentSubset, generating, currentMegaset
  #Where the new terrain starts
  if generating == -1: return 
  x = floor(origin.x + sin(radians(theta)) * rad)
  z = floor(origin.z + cos(radians(theta)) * rad)
  #Checks wether there is terrain there already
  if subDic.get('x'+ str(x) + 'z' + str(z)) != 'i':
    subCubes[currentCube].enable()
    subCubes[currentCube].x = x
    subCubes[currentCube].z = z
    subCubes[currentCube].parent = subsets[currentSubset]
    y = subCubes[currentCube].y = genPerlin(x,z,True)
    subDic['x'+ str(x) + 'z' + str(z)] = 'i'
    varch.tDic['x'+str(x)+ 'y'+str(y)+ 'z'+str(z)] = y
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
        
      # Make mega sets at the start, to make it easier to save
        # megasets.append(Entity(model=cubeModel, texture=cubeTex))
        # parent all subsets to new megaset
        for s in subsets:
          s.parent = megasets[currentMegaset]
        megasets[currentMegaset].combine(auto_destroy = False)
        for s in subsets:
          s.parent=scene
          # ???
          # s.disable()
        currentMegaset += 1
        currentSubset = 0
        print("megaset # " + str(currentMegaset))
        
  else:
    pass   
  #there was terrain already there so continue rotation to find new terrain spot
  if rad > 0:
    theta += 45/rad
  else: 
    rad += 1 
  if theta >= 360:
    theta = 0
    rad += .5



def generateShell():
  global subject, grav_speed, grav_acc

    # New 'new' system :D
    # How high or low can we step/drop?
  step_height = 3
  subjectHeight = 2
  gravityON = True
  target_y = subject.y

  for i in range(step_height,-step_height,-1):
    
      # What y is the terrain at this position?
      # terra = genPerlin(subject.x,subject.z)
    terra = varch.tDic.get( 'x'+str((floor(subject.x+ 0.5)))+
                            'y'+str((floor(subject.y+i)))+
                            'z'+str((floor(subject.z + 0.5))))
    #block one above you
    terraTop = varch.tDic.get( 'x'+str((floor(subject.x + 0.5)))+
                            'y'+str((floor(subject.y + i + 1)))+
                            'z'+str((floor(subject.z + 0.5))))
    if terra != None and terra != 'gap':
      gravityON = False
      if terraTop == 'gap' or terraTop == None:
        target_y = floor(subject.y+i) + subjectHeight
        
        break
      # if here then the tower is too tall so move subject from this position
      subject.x -= 0.6
      subject.z -= 0.6

  if gravityON==True:
    # This means we're falling!
    grav_speed += (grav_acc * time.dt) * 4
    subject.y -= grav_speed
  else:
    
    subject.y = lerp(subject.y, target_y, 9.807*time.dt)
    grav_speed = 0 # Reset gravity speed: gfloored.
    

        
  
  # old new system
  # target_y = genPerlin(subject.x, subject.z) + 2
  # target_dist = target_y - subject.y
  # # Can we step up or down
  # # if target_dist < step_height and target_dist > -step_height: 
  # subject.y = lerp(subject.y, target_y, 9.807 * time.dt)
  # elif target_dist < -step_height: #falling
    # grav_speed += (grav_acc * time.dt)
    # subject.y -= grav_speed 
  #lerp goes from one number to another in a controlled way, by time.dt multiply to standardize for different performance

 
  # global shellWidth
  # for i in range(len(shellies)):
  #   x = shellies[i].x = floor((i/shellWidth) + subject.x - 0.5 * shellWidth)
  #   z = shellies[i].z = floor((i%shellWidth) + subject.z - 0.5 * shellWidth)
  #   shellies[i].y = genPerlin(x,z)
   


chickenModel = load_model('chicken.obj')
vincent = Entity(model=chickenModel, scale = 2,
                  texture=chickenTex,
                  x = 22, z = 16, y = 4 ,
                  double_sided=True)
                  

baby = Entity(model=axoModel, scale = 2,
                  texture=axoTex,
                  x = 13, z = 12, y = 4 ,
                  color = (color.red),
                  double_sided=True)

generateShell()
  
app.run()