# this is for updating and moving character
# move up ursina import to make loading textures simpler
from ursina import *

app = Ursina()
from random import random as ra
from ursina.prefabs.first_person_controller import FirstPersonController 
from terrain_system import MeshTerrain
from flake import SnowFall
from mob_system import *
from bump_wall import *
from save_load_system import saveMap, loadMap
from inventory_system import *

#Initial Variables / imports, creations
window.color=color.rgb(0,200,225)
indra = Sky()

scene.fog_density= (0, 50)
indra.color = window.color
scene.fog_color=color.white
#subject
subject = FirstPersonController()
subject.gravity = 0.0
subject.cursor.visible = False
subject.step = 2
subject.runSpeed = 12
subject.walkSpeed = 4
subject.height=1.62 
subject.blockType = 'stone'

# property allowing us to jump
subject.frog = False
subject.jumpHeight = 3
# rate at which fov changes when dashing
camera.dash = 10


terrain = MeshTerrain(subject, camera)
generatingTerrain = True
# start with 128 * subwidth ready terrain blocks
# loadMap(subject, terrain)
for i in range(64):
    terrain.genTerrain()
snowFall = SnowFall(subject)   
# audio stuff
step_audio = Audio('step.ogg', autoplay=False, loop=False)
snow_step_audio = Audio('snowStep.mp3', autoplay=False, loop=False)

# For Earth quakes
earthCounter = 0
quaking = False
count = 0
prev_x = subject.x
prev_z = subject.z
def input(key):
    global generatingTerrain, quaking
    if key == 'q':
        app.userExit()
    elif key == 'space':
        subject.frog = True
    
    elif key == 'g':
        generatingTerrain = not generatingTerrain
    elif key == '.':
        # subjectOR = subject.rotation_y
        # subject.rotation = Vec3(0, subject.rotation_y + 10, 0)
        subject.rotation_y += 10
        # subject.rotation_y = lerp(subjectOR, subject.rotation + 10, 6 * time.dt)
    elif key == ',':
        subject.rotation_y -= 10
        # maybe lerp
    elif key == 'm':
        saveMap(subject.position, terrain.terrainDic)
    elif key == 'l':
        loadMap(subject, terrain)
    elif key == 'k':
        quaking = not quaking
        print(quaking)
    else:
        terrain.input(key)
        inv_input(key, subject, mouse)

def update():
    global count, prev_x, prev_z, earthCounter
    count += 1 
    terrain.update()
    # handle mob ai
    mob_movement(grey, subject.position, terrain.terrainDic)
  
    if count == 5:
        count = 0
        #Generate terrain at current swirl position
        # genrate a certain number of terrain chunks
        if generatingTerrain:
            # maybe you like rang 4 better
            for i in range(1):    
                terrain.genTerrain()
    
        
        # Vec3(0, 0, 1) camera.forward
        #Vec3(0, 1.86, 0) starting position
    if abs(subject.x - prev_x) > 1 or abs(subject.z - prev_z) > 1:
        prev_x = subject.x
        prev_z = subject.z
        terrain.swirlEngine.reset(prev_x, prev_z)
        if step_audio.playing == False and snow_step_audio.playing == False:
            if terrain.getDic(terrain.terrainDic, subject.x, subject.y, subject.z) == 'w':
               step_audio.pitch = 0.35 + ra()/10
            else: 
                step_audio.pitch = ra() + abs(subject.y/4)
            if subject.y > 10:
                snow_step_audio.pitch = ra() + 0.25
                snow_step_audio.play()
            else:
                step_audio.play()
    #**********************
    for h in terrain.subsets:
        if quaking == True:
            # Earthquake expereriment: sin wave through subsets to lift them up
            earth_freq = 0.5
            earthCounter += earth_freq
            earth_amplitude = 0.5
            
            h.y = h.y + (math.sin(terrain.subsets.index(h) + earthCounter) * earth_amplitude) * time.dt
        else:
            h.y = 0
        #**********************
        # Walk on solid terrain and wall collisions
    
    bumpWall(subject, terrain, quaking, h.y)
    # runnning and dash effect
    if held_keys['shift'] and held_keys['w']:
        subject.speed = subject.runSpeed
        if camera.fov < 100:
            camera.fov += camera.dash * time.dt
    else:
        subject.speed = subject.walkSpeed
        if camera.fov > 90:
            camera.fov -= camera.dash * 4 * time.dt
            if camera.fov < 90: camera.fov = 90

app.run()

