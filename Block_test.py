from DataSimulator import DataSimulator
import ECC
import MerkleTree as mtree
import Block as blk

txList = ['alice', 'carol', 'duck', 'bob']

txList.sort()
m = mtree.MerkleTree(txList)
m.generateTree()

prevHash = '9f9d51bc70ef21ca5c14f307980a29d8'

b = blk.Block(prevHash, m)
blockHash = b.mineBlock()
print('mined nonce = %s' % (blockHash))

isValid = b.validateBlock(blockHash)
if isValid:
    print('mined nonce is valid ')
else:
    print('mined nonce is not valid')
