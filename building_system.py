from ursina import Vec3, floor
"""
Our building system
"""
def checkBuild(_bsite, _terrainDic, _camF, _sub_head):
    # camF is camera forward
    #subPos is players position
    #adjust bsite for build tool entity offset. No longer have to do this because using the same model
    # create some sort of vector from the players eyes to the highlighted block.
    #l for line
    dist = _bsite - _sub_head
    j = 0.75
    mouseInWorld = _sub_head + _camF * dist.length() 
    mouseInWorld -= _camF * j
    # _bsite += Vec3(0, -0.5, 0)
    # we want to decide where to build a new block based on where we're looking
    # x = floor(_bsite.x)
    # y = floor(_bsite.y +1)
    # z = floor(_bsite.z)
    x = round(mouseInWorld.x)
    y = floor(mouseInWorld.y)
    z = round(mouseInWorld.z)
    # if we are trying to build inside bte? 
    if _bsite == Vec3(x, y, z): 
      y += 1
    #first check there isn't already terrain there y + 1 because y is one below the site
    if _terrainDic.get((x, y, z)) != 'a' and _terrainDic.get((x, y, z)) != 'g':
      if _terrainDic.get((x, y, z)) != None:
        print('Cannot build here sorry')
        return None
      
    
    # can build if we're here
    return Vec3(x, y, z)

def gapShell(_bsite, _terrainDic):
  #what position
  wp = [
          Vec3(0,1,0),
          Vec3(0,-1,0),
          Vec3(0,0,1),
          Vec3(0,0,-1),
          Vec3(1,0,0),
          Vec3(-1,0,0)
  ]
  for i in range(0,6):
    p = _bsite + wp[i]
    if _terrainDic.get((floor(p.x), floor(p.y), floor(p.z))) != 'g' or _terrainDic.get((floor(p.x), floor(p.y), floor(p.z))) != 'a':
      _terrainDic[(floor(p.x), floor(p.y), floor(p.z))] = 'g'