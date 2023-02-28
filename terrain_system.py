from ursina import *
from numpy import radians 
from perlin_noise import PerlinNoise

class Terrain:
  def __init__(this):
    #Models
    this.cubeModel = 'block.obj'
    this.cubeTex = 'block_texture.png'
    # Perlin Noise
    this.noise = PerlinNoise(octaves=1, seed=99)
     # New Terrain variables
    this.genSpeed = 0
    #generate terrain called 16 times update perloop
    this.perCycle = 64
    this.currentCube = 0
    this.numSubCubes = 64
    this.theta = 0
    this.rad = 0
    this.currentSubset = 0
    # how many combine in to a megaset
    this.numSubsets = 420
    this.radLimit = 128
    # a dictionary for recording wether terrain exist at location specified in key
    this.subDic = {}
    # terrain holders
    this.megasets = []
    this.subsets = []
    this.subCubes = []   
    this.instanciateSubCubes(this)
  
    #Instantiate ghost subset cubes
    for i in range(this.numSubCubes):
      #switching to cubeModel is not great.
      bud = Entity(model=this.cubeModel, texture=this.cubeTex)
      bud.rotation_y = random.randint(0, 4) * 90
      bud.disable()
      this.subCubes.append(bud)
      
    # Instantiate empty Subsets
    for i in range(this.numSubsets):
      bud = Entity(model=this.cubeModel)
      bud.texture = this.cubeTex
      bud.disable()
      this.subsets.append(bud)
  
  def genTerrain():
    global currentCube, theta, rad, origin, currentSubset, generating, subCubes, subDic
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
