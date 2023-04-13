from ursina import *
from random import random
from ursina.prefabs.first_person_controller import FirstPersonController 
from terrain_system import MeshTerrain
from flake import SnowFall

# this is for updating and moving character
app = Ursina()
#Initial Variables / imports, creations
window.color=color.rgb(0,200,255)
indra = Sky()
indra.color = window.color
subject = FirstPersonController()
subject.gravity = 0.0
subject.cursor.visible = False

terrain = MeshTerrain(subject.position, camera)
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
    if key == 'q':
        app.userExit()
    elif key == 'space':
        subject.y += 2
    else:
        terrain.input(key)

def update():
    global count, prev_x, prev_z
    count += 1     
    terrain.genTerrain()
    if count == 4:
        #Generate terrain at current swirl position
        terrain.update(subject.position, camera)
        count = 0
        
        # Vec3(0, 0, 1) camera.forward
        #Vec3(0, 1.86, 0) starting position
    if abs(subject.x - prev_x) > 1 or abs(subject.z - prev_z) > 1:
        prev_x = subject.x
        prev_z = subject.z
        terrain.swirlEngine.reset(prev_x, prev_z)
        if step_audio.playing == False and snow_step_audio.playing == False:
            snow_step_audio.pitch = random() + 0.25
            if subject.y <= -2:
               step_audio.pitch = 0.35 + random()/10
            else: 
                step_audio.pitch = random() + abs(subject.y/4)
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
terrain.genTerrain()
  
app.run()

