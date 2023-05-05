from ursina import Vec3, floor
from config import six_cube_dir, minerals
"""
Our building system
"""
def checkBuild(_bsite, _terrainDic, _camF, _pos):
  # camF is camera forward
  #subPos is players position
  #adjust bsite for build tool entity offset. No longer have to do this because using the same model
  # create some sort of vector from the players eyes to the highlighted block.
  dist = _bsite - _pos + Vec3(0, 1.62, 0)
 
  
  mouseInWorld = _pos + _camF * dist.length()
  mouseInWorld -= _camF * 0.75
  x = round(mouseInWorld.x)
  y = floor(mouseInWorld.y)
  z = round(mouseInWorld.z)

  print(x, y, z)
  # Oh, but what if we're trying to build inside bte?
  # Build 1 above current block! _ do we still need to do this?
  if _bsite == Vec3(x,y,z):
      y +=1
    

  #first check there isn't already terrain there y + 1 because y is one below the site
  # if _terrainDic.get((x, y, z)) != 'a' and _terrainDic.get((x, y, z)) != 'g':
  #   if _terrainDic.get((x, y, z)) != None:
  if _terrainDic.get((x, y, z)) in minerals:
      print('Cannot build here sorry')
      return None
    
  
  # can build if we're here
  return Vec3(x, y, z)

def gapShell(_bsite, _terrainDic):

  #what position
 
  for i in range(0,6):
    p = _bsite + six_cube_dir[i]
    if _terrainDic.get((floor(p.x), floor(p.y), floor(p.z))) in minerals:
      _terrainDic[(floor(p.x), floor(p.y), floor(p.z))] = 'g'