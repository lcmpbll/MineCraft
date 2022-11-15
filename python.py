from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from numpy import floor
from perlin_noise import PerlinNoise

app = Ursina()
 #window
window.color = color.rgb(0, 200, 211)
window.exit_button.visible = False
window.fullscreen = False
scene.fog_color = color.rgb(255, 0 , 0 )
scene.fog_density = 0.04
# Texture make lighter on the outside
grassStrokeTex = load_texture('grass.png')
def input(key):
  if key == 'q' or key == 'escape':
    quit()
 
def update():
  pass  
 
 # terrain  
terrain = Entity(model=None, collider=None)
noise = PerlinNoise(octaves=2, seed=2022)
amp = 6
freq = 24
  
  # 100 block cubes            
terrainWidth = 50
for i in range(terrainWidth * terrainWidth):
  bud = Entity(model='cube', color=color.green,)
              #makes rows and columns
  bud.x = floor(i/terrainWidth)
  bud.z = floor(i%terrainWidth)
  bud.y = floor((noise([bud.x/freq,bud.z/freq])) * amp)
  bud.parent = terrain
terrain.combine()
terrain.collider = 'mesh'
terrain.texture = grassStrokeTex
  # collider for all cubes
  
  
  
subject = FirstPersonController()
subject.cursor.visible = False
subject.gravity = .5
# can set two variables at the same time
subject.x = subject.z = 5
subject.y = 12
  
app.run()
