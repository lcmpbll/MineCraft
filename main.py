from ursina import *
from random import random as ra
from ursina.prefabs.first_person_controller import FirstPersonController 
from terrain_system import MeshTerrain
from flake import SnowFall
from mob_system import *

# this is for updating and moving character
app = Ursina()
#Initial Variables / imports, creations
window.color=color.rgb(0,200,255)
indra = Sky()
indra.color = window.color
subject = FirstPersonController()
subject.gravity = 0.0
subject.cursor.visible = False
subject.step = 2
subject.jumpHeight = 3

terrain = MeshTerrain(subject.position, camera)
generatingTerrain = True
# start with 128 * subwidth ready terrain blocks
for i in range(64):
    terrain.genTerrain()
snowFall = SnowFall(subject)   
# audio stuff
step_audio = Audio('step.ogg', autoplay=False, loop=False)
snow_step_audio = Audio('snowStep.mp3', autoplay=False, loop=False)
# create and hold flakes
# flakes = []
# def generateFlakes():
    
#     for i in range(128):
#         e = Flake(subject.position)
#         flakes.append(e)
count = 0
prev_x = subject.x
prev_z = subject.z
def input(key):
    global generatingTerrain
    if key == 'q':
        app.userExit()
    elif key == 'space':
        subject.y += 2
    elif key == 'g':
        generatingTerrain = not generatingTerrain
    elif key == '.':
        #wip
        currentLeft = subject.left
        subject.forward = currentLeft
        camera.forward = subject.right
        
        print(camera.forward) 
        # sub.forward Vec3(-0.993681, 0, 0.11224)
        # camera.forward Vec3(0, 0, 1)
    else:
        terrain.input(key)

def update():
    global count, prev_x, prev_z
    count += 1 
    terrain.update(subject.position, camera)
    # handle mob ai
    mob_movement(grey, subject.position, terrain.terrainDic)
  
    if count == 5:
        count = 0
        #Generate terrain at current swirl position
        # genrate a certain number of terrain chunks
        if generatingTerrain:
            for i in range(4):    
                terrain.genTerrain()
    
        
        # Vec3(0, 0, 1) camera.forward
        #Vec3(0, 1.86, 0) starting position
    if abs(subject.x - prev_x) > 1 or abs(subject.z - prev_z) > 1:
        prev_x = subject.x
        prev_z = subject.z
        terrain.swirlEngine.reset(prev_x, prev_z)
        if step_audio.playing == False and snow_step_audio.playing == False:
            snow_step_audio.pitch = ra() + 0.25
            if subject.y <= -2:
               step_audio.pitch = 0.35 + ra()/10
            else: 
                step_audio.pitch = ra() + abs(subject.y/4)
            if subject.y > 4:
                snow_step_audio.play()
            else:
                step_audio.play()
    blockFound = False
    step = 2
    height = 1.86
    # Technically flooring twice, but prevents shaking
    x = floor(subject.x + 0.5)
    y = floor(subject.y + 0.5)
    z = floor(subject.z + 0.5)
    for i in range(-step, step):
        if terrain.getDic(terrain.terrainDic, x, y + i, z) == 't': 
            if terrain.getDic(terrain.terrainDic, x, y+i + 1, z) == 't':
                target = y + i + 1 + height
                blockFound = True
                break    
            target = y + i + height
            blockFound = True
            break
    if blockFound == True: 
        # step up or down : >
        subject.y = lerp(subject.y, target, 6 * time.dt)
    else: 
        #gravity fall : <
        subject.y -= 9.8 * time.dt 
    pass

app.run()

