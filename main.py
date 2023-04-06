from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController 
from terrain_system import MeshTerrain

# this is for updating and moving character
app = Ursina()
#Initial Variables / imports, creations
window.color=color.rgb(200,0,255)
subject = FirstPersonController()
subject.gravity = 0.0
terrain = MeshTerrain()

def input(key):
    if key == 'q':
        app.userExit()

def update():
    pass
terrain.genTerrain()
  
app.run()

