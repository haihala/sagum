class Object():
    def __init__(self, pos, img):
        self.pos = pos
        self.img = img
        self.rect = []

def fromSafe(string):
    string = string.strip()
    s = string.split(",")
    ret = Object((int(s[2]), int(s[1])), s[0])
    return ret
