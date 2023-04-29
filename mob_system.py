from ursina import *



grey = FrameAnimation3d('panda_walk_', fps=1)
#WIP texture
grey.texture='panda_texture'
# grey.position = copy(subject.position) + Vec3(-6, -1, 9)
grey.position = Vec3(-6, -1, 9)
grey.turnSpeed = 2
grey.speed = 1
grey.step = 4
grey.canSwim = False
grey.isChasing = False
grey.chaseDistance = 8
grey.intamacyDistance = 3
grey.sub = False

def mob_movement(mob, _subjectPos, _terrainDic):
  #WIP chasing
  dist = _subjectPos - mob.position
  print(_terrainDic.get((floor(mob.position.x), floor(mob.position.y), floor(mob.position.z))))
  if _terrainDic.get((floor(mob.position.x), floor(mob.position.y), floor(mob.position.z))) == 'w' and mob.canSwim == False:
    mob.isChasing = False
  

  if dist.length() > mob.chaseDistance:
    mob.isChasing = False
    mob.is_playing = False
    mob.pause()
  elif dist.length() < mob.intamacyDistance:
    mob.isChasing = False
    mob.is_playing = False
    mob.pause()
  else:
    mob.isChasing = True
  #turn speed not affected? BUG
  if mob.isChasing == True:
    tempOR = mob.rotation_y
    mob.lookAt(_subjectPos)
    mob.rotation = Vec3(0, mob.rotation_y + 180, 0)
    mob.rotation_y = lerp(tempOR, mob.rotation_y, mob.turnSpeed * time.dt)
    # now move towards target
    mob.position -= mob.forward * mob.speed * time.dt
    mob.resume()
    mob.is_playing = True
  elif mob.isChasing == False and dist.length() > mob.intamacyDistance:
    #add count to only change lookat infrequently
    tempOR = mob.rotation_y
    mob.lookAt(findLand(mob, _terrainDic))
    mob.rotation = Vec3(0, mob.rotation_y + 180, 0)
    mob.rotation_y = lerp(tempOR, mob.rotation_y, mob.turnSpeed * time.dt)
    mob.position -= mob.forward * mob.speed * time.dt
    mob.resume()
    mob.is_playing = True
  terrain_walk(mob, _terrainDic)
    

def terrain_walk(mob, _terrainDic):
  blockFound = False
  # add in variable to swich blocks and go somewhere else if water.
  height = 1
  if mob.y < -100:
      mob.y = 100
      print("Help I've fallen")
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
      elif _terrainDic.get((x, y + i, z)) == 'w':
          
          if mob.canSwim == True:
              # mob.rotation = Vec3(0, mob.rotation_y - 90, 0)
              mob.position -= mob.forward * mob.speed * time.dt
              
              mob.y = lerp(mob.y, -1, 6 * time.dt)
          if mob.canSwim == False: 
            print('help, I cant swim')
            for j in range(-mob.step, mob.step):
              if _terrainDic.get((x + j, y + i, z)) == 't':
                target = (x + j, y + i, z)
                # mob.rotation = Vec3(0, mob.rotation_y - (45 * i), 0)
                mob.position -= mob.back * mob.speed * time.dt
                mob.position = lerp(mob.position, target, 6 * time.dt)
              
              
              elif _terrainDic.get((x, y + i, z + j)) == 't':
                
                  # mob.rotation = Vec3(0, mob.rotation_y - (45 * i), 0)
                  mob.position -= mob.back * mob.speed * time.dt
                  target = (x, y + i, z + j)
                  mob.position = lerp(mob.position, target, 6 * time.dt)
              else:
                # sink
                mob.y = lerp(mob.y, -2, 6 * time.dt)
             
  if blockFound == True: 
      # step up or down : >
      mob.y = lerp(mob.y, target, 6 * time.dt)
  else:      #gravity fall : <
      mob.y -= 9.8 * time.dt 

def findLand(mob, _terrainDic):
   # BUG still not avoiding water
   for i in range(-10, 10):
      for j in range(-10, 10):
         for k in range(-mob.step, mob.step):
          if _terrainDic.get((floor(mob.position.x + i), floor(mob.position.y + k), floor(mob.position.z + j))) == 't':
            return Vec3(floor(mob.position.x + i), floor(mob.position.y + k), floor(mob.position.z + j))
           
          