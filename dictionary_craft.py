from ursina import floor
class DictionaryCraft:
    def __init__(this):
      pass
    def getDictionary(this, dic, _x, _y, _z):
        return dic.get((floor(_x), floor(_y), floor(_z)))
    def recDictionary(this, dic, _x, _y, _z, _rec):
        dic[(floor(_x), floor(_y), floor(_z))] = _rec
