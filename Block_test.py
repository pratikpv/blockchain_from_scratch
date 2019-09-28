# CS266: Fall 2019
# HW1
#
# Pratik Prajapati
# Ashraf Saber
#

import MerkleTree as mtree
import Block as blk

# a test script to check various functions of the Block() class.
#
txList = ['alice', 'carol', 'duck', 'bob']

txList.sort()
m = mtree.MerkleTree(txList)
m.generateTree()

# just any random hash to test
prevHash = '9f9d51bc70ef21ca5c14f307980a29d8'

b = blk.Block(prevHash, m)
blockHash = b.mineBlock()
print('mined nonce = %s' % (blockHash))
