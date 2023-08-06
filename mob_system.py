from ursina import *
from config import minerals

# demonKat = FrameAnimation3d('panda_walk_', fps=1)
grey = FrameAnimation3d('panda_walk_', fps=1)

# demonKat.texture = 'tex_demonikat'
katText = load_texture('tex_demonikat.png')
demonikat = Entity(model='demonikat.obj', scale=2, texture=katText)

grey.texture='panda_texture'
# grey.position = copy(subject.position) + Vec3(-6, -1, 9)
# static for reset
demonikat.startPoint = Vec3(-6, -1, 9)
demonikat.position = Vec3(-8, 1, 30)
demonikat.turnSpeed = 4
demonikat.speed = 3
demonikat.step = 6
demonikat.canSwim = False
demonikat.isChasing = False
demonikat.chaseDistance = 30
demonikat.intamacyDistance = 3
demonikat.sub = False
demonikat.onGround = False
demonikat.gravity = 0
demonikat.speed = 0

grey.startPoint = Vec3(-6, -1, 9)
grey.position = Vec3(-6, -1, 9)
grey.turnSpeed = 2
grey.speed = 1
grey.step = 4
grey.canSwim = False
grey.isChasing = False
grey.chaseDistance = 8
grey.intamacyDistance = 3
grey.sub = False

#WIP
def mob_on_ground(mob, _terrainDic):
  if mob.onGround == True:
   
    pass
  else:
    if _terrainDic.get((floor(mob.position.x), floor(mob.position.y), floor(mob.position.z))) in minerals:
      
      mob.onGround = True
      mob.gravity = 0
      
    else:
      print(mob.position.y)
      print(mob.onGround)
      mob.position.y -= 1
       
      
      

def mob_movement(mob, _subjectPos, _terrainDic):
  #WIP chasing
  dist = _subjectPos - mob.position
  mobTerrainSpot =_terrainDic.get((floor(mob.position.x), floor(mob.position.y), floor(mob.position.z)))
  thingToLookAt = _subjectPos
  if mob.isChasing == False and dist.length() > mob.intamacyDistance:
    thingToLookAt = findLand(mob, _terrainDic)
  
  if thingToLookAt == None:
    thingToLookAt = mob.startPoint
  
  # turn off chasing if mob is in the water and can't swim
  if _terrainDic.get((floor(mob.position.x), floor(mob.position.y), floor(mob.position.z))) == 'w' and mob.canSwim == False:
    mob.isChasing = False
  # turn off chasing if mob is too far or too close

  elif dist.length() > mob.chaseDistance:
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
    mob.lookAt(thingToLookAt)
    mob.rotation = Vec3(0, mob.rotation_y + 180, 0)
    mob.rotation_y = lerp(tempOR, mob.rotation_y, mob.turnSpeed * time.dt)
    # now move towards target
    mob.position -= mob.forward * mob.speed * time.dt
    mob.resume()
    mob.is_playing = True
  elif mob.isChasing == False and dist.length() > mob.intamacyDistance:
    #add count to only change lookat infrequently
    tempOR = mob.rotation_y
    mob.lookAt(thingToLookAt)
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
      
      if _terrainDic.get(( x, y + i, z)) in minerals: 
          if _terrainDic.get(( x, y+i + 1, z)) in minerals:
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
              currentTX = _terrainDic.get((x + j, y + i, z))
              if currentTX != 'a' and currentTX != 'g' and currentTX != 'w':
                target = (x + j, y + i, z)
                # mob.rotation = Vec3(0, mob.rotation_y - (45 * i), 0)
                mob.position -= mob.back * mob.speed * time.dt
                mob.position = lerp(mob.position, target, 6 * time.dt)
              
              
              elif _terrainDic.get((x, y + i, z + j)) in minerals:
                
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
  x = floor(mob.x + 0.5)
  y = floor(mob.y + 0.5)
  z = floor(mob.z + 0.5)
  for i in range(-10, 10):
    for j in range(-10, 10):
        for k in range(-mob.step, mob.step):
          if _terrainDic.get((floor(x + i), floor(y + k), floor(z + j))) in minerals:
            return Vec3(floor(x + i), floor(y + k), floor(z + j))
          
          
          