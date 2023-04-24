from ursina import *

hotbar = Entity(model='quad', parent=camera.ui, texture='white_box.png')
# set size and position
hotbar.scale_y = 0.1
hotbar.scale_x = 0.8
hotbar.position.y = -0.5 + (hotbar.scale_y * 0.5)
# set appearance
hotbar.color = color.dark_gray

def inv_input(key, subject, mouse):
  if key == 'e' and subject.enable:
    subject.disable()
    mouse.locked = False
  elif key == 'e' and not subject.enable:
    mouse.locked = True
    subject.enable() 


