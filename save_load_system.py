"""
Saving and loading terrain map
currently not working, could have to do with checkwater?
"""
from config import minerals

mapName = 'june_test_1.land'

def saveMap(_subPos, _terrainDic):
  import os, sys, pickle
  #open main module directory to find the correct path
  path = os.path.dirname(os.path.abspath(sys.argv[0]))
  os.chdir(path)
  # handles errors with  || write bytes
  with open('test_map2.panda', 'wb') as f:
    map_data = [_subPos, _terrainDic]
    pickle.dump(map_data, f)
    map_data.clear()
    
def loadMap(_subject, _terrain):
  import os, sys, pickle, copy
  from ursina import destroy
  # Open main module to 
  path = os.path.dirname(os.path.abspath(sys.argv[0]))
  os.chdir(path)
  with open('test_map2.panda', 'rb') as f:
    map_data = pickle.load(f)
   
  #empty out current terrain subesets
  for s in _terrain.subsets:
    destroy(s)
  
  _terrain.terrainDic= {}
  _terrain.vertexDic = {}
  _terrain.subsets = []
  _terrain.setup_subsets()
  _terrain.currentSubset = 1
  _terrain.terrainDic = copy.copy(map_data[1])
  
  # iterate over the terrain dictionary 
  
  i = 0 # which subset to build block on
  for key in _terrain.terrainDic:
    whatT = _terrain.terrainDic.get(key)
    if whatT != None and whatT != 'g' and whatT != 'a':
      x = key[0]
      y = key[1]
      z = key[2]
      if i >= len(_terrain.subsets)-1:
        i = 0
      _terrain.genBlock(x, y, z, subset = i, mining=False, blockType = whatT)
      i += 1
  
  _subject.position = copy.copy(map_data[0])
  _terrain.swirlEngine.reset( _subject.position.x, _subject.position.z )
  # Regenerate subset model so that we can see the terrain
  for s in _terrain.subsets:
    s.model.generate()

"""
Saving and loading a terrain 'map'.
"""

# mapName='june_test_1.land'

# def saveMap(_subPos, _td):
#     import os, sys, pickle

#     # Open main module directory for correct file.
#     path = os.path.dirname(os.path.abspath(sys.argv[0]))
#     os.chdir(path)

#     with open(mapName, 'wb') as f:

#         map_data = [_subPos, _td]

#         pickle.dump(map_data, f)

#         map_data.clear()

# def loadMap(_subject,_terrain):
#     import os, sys, pickle
#     from ursina import destroy

#     # Open main module directory for correct file.
#     path = os.path.dirname(os.path.abspath(sys.argv[0]))
#     os.chdir(path)
#     with open(mapName, 'rb') as f:
#         map_data = pickle.load(f)

#     # Empty out current terrain objects.
#     for s in _terrain.subsets:
#         destroy(s)
#     _terrain.terrainDic={}
#     _terrain.vertexDic={}
#     _terrain.subsets=[]
#     _terrain.setup_subsets()
#     _terrain.currentSubset=1
#     # Without copy?
#     _terrain.terrainDic=map_data[1]
#     # Iterate over terrain dictionary and
#     # if we find 't' then generate a block.
#     # Note this means we'll lose colour info etc.
#     i = 0 # Which subset to build block on?
#     for key in _terrain.terrainDic:
#         whatT=_terrain.terrainDic.get(key)
#         if whatT!=None and whatT!='g':
#             x = key[0]
#             y = key[1]
#             z = key[2]
#             if i>=len(_terrain.subsets)-1:
#                 i=0
#             _terrain.genBlock(x,y,z,subset=i,mining=False,blockType=whatT)
#             i+=1

#     # And reposition subject according to saved map.
#     _subject.position=map_data[0]
#     # Reset swirl engine.
#     _terrain.swirlEngine.reset( _subject.position.x,
#                                 _subject.position.z)
#     # Regenerate subset models, so that we can see terrain.
#     for s in _terrain.subsets:
#         s.model.generate()