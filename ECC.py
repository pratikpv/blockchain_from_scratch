#self made ECC library
#used to teach basic elements
#
# DO NOT USE FOR REAL CRYPTOGRAPHY
#

import random as RNG
import math
import hashlib

def random(maxint):
    return int(RNG.random() * maxint)

def isPrime(n):
    for i in range(int(math.sqrt(n))-1):
        if n % (i+2) == 0:
            return False
    return True


def simpleHash(txt, n):
    #z= (reduce(lambda a,b: a+b, [ord(c) for c in txt], 0)) % (n-1)
    sum = 0
    for c in txt:
        sum += ord(c)
    z = sum % (n-1)

    return z+1

hash = lambda x: hashlib.md5(x.encode('utf-8')).hexdigest()
#extended greatest common denominator

def egcd(a, b):
    """extended greatest common denominator
    returns the GCD and (if GCD == 1) the bezout coefficients x,y
    so that xa+by = 1
    """
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)


def invModN(a,n):
    "computes the inverse a^-1 % p, i.e. a number b so that a*b==1 mod p"
    gcd, x, y = egcd(a, n)
    if gcd!=1:
        return 0
    else:
        return x % n

class Curve:
    def __init__(self, groupOrder, a, b):
        self.groupOrder = groupOrder
        self.a = a
        self.b = b

    def newRandomPoint(self):
        validPoint = False
        x = 0
        y = 0
        while (not validPoint):
            x = random(self.groupOrder)
            y = random(self.groupOrder)
            if (self.validPoint(x,y)):
                return (x, y)

    def inverse(self, a):
        "computes the inverse a^-1 % p, i.e. a number b so that a*b==1 mod p"
        gcd, x, y = egcd(a, self.groupOrder)
        if gcd!=1:
            print("Group order is not prime or point not on curve")
            print(a,gcd, x, y)
            return -1
        else:
            return x % self.groupOrder

    def gradientBetween(self, x1, y1, x2, y2):
        """ Compute the slope of the line between two points (x1, y1) and (x2, y2)"""
        if (x2-x1 > 0):
            return (y2 - y1) * self.inverse(x2 - x1)
        else:
            if (x1 == x2):
                pass
            return (y1 - y2) * self.inverse(x1 - x2)

    def gradientAt(self, x, y):
        """ Compute the slope (i.e. the tangent) at the point (x1, y1)"""
        return ((3*x*x + self.a) * self.inverse(2*y)) % self.groupOrder

    def validPoint(self, x, y):
        lhs = (y*y) % self.groupOrder
        rhs = (x*x*x + self.a*x + self.b) % self.groupOrder
        if (lhs == rhs):
            return True
        #print((lhs, rhs))
        return False



class Point:
    def __init__(self, groupOrder, a, b, coords=None):
        self.curve = Curve(groupOrder, a, b)
        if coords is None:
            #random new point with prime group order

            goodPoint = False
            while not goodPoint:
                self.coord = self.curve.newRandomPoint()
                n=1
                while (n*self).coord != (0,0):
                    n+=1

                if isPrime(n):
                    self.n = n
                    #print "goodPoint: (%i, %i), order %i" % (self.coord[0],self.coord[1], self.n)
                    goodPoint = True

        else:
            self.coord = coords
            self.n = None # at least not yet computed

    def __add__(self, other):
        x1, y1 = self.coord
        x2, y2 = other.coord


        if (self.coord == other.coord):
            #point doubling
            gradient = self.curve.gradientAt(x1, y2)
        else:
            if(x1==x2):
                return Point(self.curve.groupOrder, self.curve.a, self.curve.b, (0, 0))
            gradient = self.curve.gradientBetween(x1, y1, x2, y2)

        x3 = (gradient*gradient - x2 - x1) % self.curve.groupOrder
        y3 = ((gradient*(x2-x3)-y2)) % self.curve.groupOrder
        return Point(self.curve.groupOrder, self.curve.a, self.curve.b, (x3, y3))

    def __rmul__(self, other):
        if (other == 1):
            return self
        if (other == 0):
            return (0,0)
        if (other < 0):
            print("subtraction not implemented")
            return self

        newPoint = None
        target = other
        doubling = self
        while (target>0):
            if target % 2:
                if newPoint is None:
                    newPoint = doubling
                else:
                    newPoint = newPoint + doubling

            doubling = doubling + doubling
            target = target >> 1

        return newPoint

    def to_a(self):
        return [self.curve.groupOrder, self.curve.a, self.curve.b, self.coord]






class SimpleECC:
    def __init__(self, basepoint):
        self.basePoint = basepoint
        self.sk = random(basepoint.curve.groupOrder)
        self.pk = self.sk * self.basePoint

        if self.basePoint.n is None:
            n=1
            while (n*self.basePoint).coord != (0,0):
                n+=1
            self.n = n
        else:
            self.n = self.basePoint.n


    def exportKey(self):
        curve = self.basePoint.curve
        try:
            return "Curve( %i %i %i ); G( %i %i ); PK( %i %i ); PKOrder( %i )" % \
                (curve.groupOrder, curve.a, curve.b,
                self.basePoint.coord[0], self.basePoint.coord[1],
                self.pk.coord[0], self.pk.coord[1],
                self.n)
        except:
            return "invalid Signature"




    def sign(self, message):
        n = self.n
        z = simpleHash(message, n)

        valid = False
        r = 0
        k = 0
        while (not valid):

            k = random(n-1)+1
            newPoint = k*self.basePoint
            r = newPoint.coord[0] % n

            if r != 0:
                s = (invModN(k, n) * (z + (self.sk*r))) % n

                if s != 0:
                        if (invModN(s,n) != 0):
                            return (r,s)



def verify(pubKeyString, message, signature):
    #import ipdb; ipdb.set_trace()
    try:
        keySplits = pubKeyString.split(" ")
        assert (len(keySplits)==16)

        # 'Curve( 397 -2 2 ); G( 344 30 ); PK( 45 282 ); PKOrder( 375 )'

        curveOrder = int(keySplits[1])
        curveA = int(keySplits[2])
        curveB = int(keySplits[3])
        assert(curveOrder > 0)

        baspointX = int(keySplits[6])
        baspointY = int(keySplits[7])
        assert(baspointX > 0)
        assert(baspointY > 0)

        pkX = int(keySplits[10])
        pkY = int(keySplits[11])
        n = int(keySplits[14])
        assert(pkX > 0)
        assert(pkY > 0)
        assert(n > 0)
    except:
        #print "pubKeyString invalid: >>%s<<" % pubKeyString
        return False

    try:
        pubKey = Point(curveOrder, curveA, curveB, (pkX, pkY))

        basepoint = Point(curveOrder, curveA, curveB, (baspointX, baspointY))
        if(pubKey.coord == (0,0)):
            return False
        if not (pubKey.curve.validPoint(pubKey.coord[0], pubKey.coord[1])):
            return False

        r,s = signature
        s=s
        #n = pubKey.curve.groupOrder
        if (r<1 or r>= n or s<1 or s>=n):
            return False
        z = simpleHash(message, n)
        s_inv = invModN(s, n)
        u1 = (z*s_inv) % n
        u2 = (r*s_inv) % n

        point = u1*basepoint + u2*pubKey


        if(point.coord == (0,0)):
            return False

        if (((point.coord[0] % n) + n) % n) == (((r % n) + n) % n):
            return True
        return False
    except:
        return False
