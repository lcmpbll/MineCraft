from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController 
from terrain_system import MeshTerrain

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
    if abs(subject.x - prev_x) > 4 or abs(subject.z - prev_z):
        prev_x = subject.x
        prev_z = subject.z
        terrain.swirlEngine.reset(prev_x, prev_z)
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

