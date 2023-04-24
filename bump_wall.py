
from ursina import Vec3, held_keys, time, lerp
# all things using this system must have height, step height, and jumpheight
# maybe canSwim

   
def bumpWall(subject, terrain):
  blockFound = False
  step = subject.step
  jumpHeight = subject.jumpHeight
  height = subject.height
  x = round(subject.x)
  z = round(subject.z)
  y = round(subject.y)
  #simple wall collision detection
  # front and back
  # inF iss location of blocks ahead, behind and side
  def checkBump(inF):
    for i in range(1, step + 1):
      whatT = terrain.terrainDic.get((round(inF.x), round(inF.y + 1), round(inF.z)))
      if whatT != None and whatT != 'a' and whatT != 'g':
        return True
      return False
      #if whatT == 'w
  # In front...
  # Also check diagonal left and right...
  howClose  = 0.55
  rPos = Vec3(x, y, z)
  subFor = subject.forward
  subFor.y = 0
  # ahead

  bDir = rPos + subFor * howClose #bump direction 
  if(checkBump(bDir) or 
     checkBump(bDir + subject.left * howClose * 0.5) or 
     checkBump(bDir + subject.right * howClose * 0.5)):
    held_keys['w'] = 0
  # behind
  bDir = rPos - subFor * howClose
  if(checkBump(bDir) or
    checkBump(bDir + subject.left * howClose * 0.5) or 
    checkBump(bDir + subject.right * howClose * 0.5)):
    held_keys['s'] = 0
  # Left
  subLat = subject.left
  subLat.y = 0
  bDir = rPos - subLat * howClose
  if(checkBump(bDir) or 
     checkBump(bDir + subject.forward * howClose * 0.5) or 
     checkBump(bDir + subject.back * howClose * 0.5)):
    held_keys['a'] = 0
  # Right
  bDir = rPos - subLat * howClose
  if(checkBump(bDir) or
    checkBump(bDir + subject.forward * howClose * 0.5) or 
    checkBump(bDir + subject.back * howClose * 0.5)):
    held_keys['d'] = 0
      
  # Walking on the terrain itself.
 # walk on top of water
  for i in range(-2,step):
      whatT1=terrain.terrainDic.get((x,y+i,z))
      if whatT1!=None and whatT1!='g' and whatT1 != 'a':
          whatT2=terrain.terrainDic.get((x,y+i+1,z))
          if whatT2!=None and whatT2!='g' and whatT2 != 'a':
              # Also check any blocks above, still within stepping range.
              target = y+i+height+1
              blockFound=True
              break
          # Stomach height?
          whatT3=terrain.terrainDic.get((x,y+i+2,z))
          if whatT3!=None and whatT3!='g' and whatT3 != 'a':
              target = y+i+height+2
              blockFound=True
              break
          target = y+i+height
          blockFound=True
          break
  if blockFound==True:
      
      # Step up or down :>
      subject.y = lerp(subject.y, target, 6 * time.dt)
      # We are grounded -- so can jump...
      if subject.frog is True:
          subject.frog=False
          subject.y+=jumpHeight
  else:
      # Gravity fall :<
      subject.y -= 9.8 * time.dt
