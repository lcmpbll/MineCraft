from ursina import *



grey = FrameAnimation3d('panda_walk_', fps=1)
#guy = Entity(model='panda_mod', texture='panda_tex')
grey.texture = 'panda_tex.png'
# grey.position = copy(subject.position) + Vec3(-6, -1, 9)
grey.position = Vec3(-6, -1, 9)
grey.turnSpeed = 0.2
grey.speed = 1
grey.step = 4
grey.canSwim = False
grey.isChasing = False
grey.chaseDistance = 8

def mob_movement(mob, _subjectPos, _terrainDic):
  #WIP chasing
  dist = _subjectPos - mob.position
  print(mob.isChasing)
  if dist.length() > mob.chaseDistance:
    mob.isChasing = False
    mob.is_playing = False
    mob.pause()
  else:
    mob.isChasing = True
  #turn speed not affected? BUG
  if mob.isChasing == True:
    mob.lookAt(_subjectPos, mob.turnSpeed * time.dt)
    mob.rotation = Vec3(0, mob.rotation_y + 180, 0)
    # now move towards target
    mob.position -= mob.forward * mob.speed * time.dt
    mob.resume()
    mob.is_playing = True
  terrain_walk(mob, _terrainDic)
    

def terrain_walk(mob, _terrainDic):
    blockFound = False
    
    height = 1
    # Technically flooring twice, but prevents shaking
    x = floor(mob.x + 0.5)
    y = floor(mob.y + 0.5)
    z = floor(mob.z + 0.5)
    for i in range(-mob.step, mob.step):
        if _terrainDic.get(( x, y + i, z)) == 't': 
            if _terrainDic.get(( x, y+i + 1, z)) == 't':
                target = y + i + 1 + height
                blockFound = True
                break    
            target = y + i + height
            blockFound = True
            break
        elif _terrainDic.get((x, y, z)) == 'w':
            if mob.canSwim == False:
                mob.rotation = Vec3(0, mob.rotation_y + 180, 0)
                mob.position -= mob.forward * mob.speed * time.dt
    if blockFound == True: 
        # step up or down : >
        mob.y = lerp(mob.y, target, 6 * time.dt)
    else: 
        #gravity fall : <
        mob.y -= 9.8 * time.dt 