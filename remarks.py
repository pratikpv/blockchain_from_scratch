# The data is provided via a class DataSimulator

import DataSimulator as DSim

DS = DSim.DataSimulator()

# The object DS provides a function
# getNewData() that can be called
# repeatedly to simulate the newly
# received information

newData = DS.getNewData()
print newData
#
# This is list of dict types, each of them of the form
# {
#     "msg"       : str         # the message
#     "pk"        : str         # the public key
#     "signature" : [int, int]  # the ECC signature (a point on the curve)
# }
# the public key pk is given as readable list of parameters
# Curve( 463 -2 2 ); G( 155 452 ); PK( 424 5 ); PKOrder( 149 )
# Thus, the curve is
# x^3 -2x + 2 % 463 == y^2 % 463
# with
#  - a base point G=(155, 452),
#  - public key point P=(424, 5) and
#  - the order of the sub-group induced by G is 149, i.e. 149*G = (0,0)


# Let's look at a single element of the received data

d = newData[20]
print d

# To verify the signature, we need to import the ECC module for actual curve operations

import ECC

# Let's check whether this signature is correct. The verify function is
#
#   ECC.verify(pubKeyString, message, signature)
#
# hence we call it with the public key string d['pk'], the message and the signature

print ECC.verify(d['pk'], d["msg"], d["signature"])
# True

# Or, if we write down the parameters explicitly
print ECC.verify(d['pk'], "cabinet meets to balance budget priorities", (9,30))
# True


# Thus evaluates to True. If we change the message a bit (cabinet -> Cabinet), we get
print ECC.verify(d['pk'], "Cabinet meets to balance budget priorities", (9,30))
# False

# And finally, for the Merkle Tree
# of all valid entries, we need to
# be able to hash an element. We
# use the str function, provided
# by Python

print (str(d))
# -> "{u'msg': u'cabinet meets to balance budget priorities', u'pk': u'Curve( 463 -2 2 ); G( 155 452 ); PK( 263 231 ); PKOrder( 149 )', u'signature': [9, 30]}"


# And this string can be given to ECC.hash(s)

print ECC.hash(str(d))
