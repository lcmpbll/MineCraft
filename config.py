"""
Were we set up default values as well as handly lists and dictionaries.
"""
from ursina import Vec3, Vec4
six_cube_dir = [
  Vec3(0, 1, 0),
  Vec3(0, -1 , 0),
  Vec3(-1, 0, 0),
  Vec3(1, 0, 0),
  Vec3(0, 0, -1),
  Vec3(0, 0, 1)
]

minerals = {
    'grass': (8,7),
    'soil': (10,7),
    'stone': (8,5),
    'concrete': (9,6),
    'ice': (9, 7),
    'water': (9,7),
    'snow': (8,6),
    'ruby': (9,6, Vec4(1,0,0,1)),
    'emerald': (9,6, Vec4(0,0.8,0, 0.8)), 
    'wood': (11,7),
    'foilage': (11,6)
}

mins = list(minerals.keys())