from ursina import Vec3, floor
"""
Our building system
"""
def checkBuild(_bsite, _terrainDic):
    #adjust bsite for build tool entity offset.
    _bsite += Vec3(0, -0.5, 0)
    x = floor(_bsite.x)
    y = floor(_bsite.y +1)
    z = floor(_bsite.z)
    #first check there isn't already terrain there y + 1 because y is one below the site
    if _terrainDic.get((x, y, z)) != 'a' and _terrainDic.get((x, y, z)) != 'g':
      if _terrainDic.get((x, y, z)) != None:
        print(_terrainDic.get((x, y, z)))
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