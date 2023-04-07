from ursina import floor
class DictionaryCraft:
    def __init__(this):
      pass
    def getDictionary(this, dic, _x, _y, _z):
        return dic.get('x' + str(floor(_x)) + 'y' + str(floor(_y)) + 'z' + str(floor(_z)))
    def recDictionary(this, dic, _x, _y, _z, _rec):
        dic['x' + str(floor(_x)) + 'y' + str(floor(_y)) + 'z' + str(floor(_z))] = _rec
    def parseForDic(this, _x, _y, _z):
        return 'x' + str(floor(_x)) + 'y' + str(floor(_y)) + 'z' + str(floor(_z))