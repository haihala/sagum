import random
from object import *
from pickle import *
import sys
import os

def loadMap(name):
    objects = []
    hand = open("maps/" + name, "rb")
    pf = load(hand)  # pickle file
    for line in pf.split("\n"):
        if len(line) != 0:
            objects.append(fromSafe(line))
    hand.close()
    return objects

def saveMap(name, objects):
    hand = open(name, "wb")
    ds = ""
    for i in objects: ds += str(i)
    dump(ds, hand)
    hand.close()

def mkMap(amount):
    m = []  # the generated map
    structures = []
    for s in os.listdir("art/structures"): structures.append(s)  # lists structures in the art folder
    for i in range(amount): m.append(random.choice(structures) + ", " + str(random.randint(0, 10000)) +", " + str(random.randint(0, 10000)) + "\n")
    saveMap("maps/Sg_def.map", m)


if __name__ == "__main__":
    if (len(sys.argv)) == 1:
        mkMap(4)
    elif len(sys.argv) == 2:
        mkMap(sys.argv[1])
    else:
        print "usage: python mapper.py [amount of objects]\nAmount argument is optional"
