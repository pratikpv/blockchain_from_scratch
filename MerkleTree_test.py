from DataSimulator import DataSimulator
import ECC
import MerkleTree as mtree

list = ['alice', 'carol', 'duck', 'bob']

list.sort()
m = mtree.MerkleTree(list)
m.generateTree()
m.postOrderPrintTree()
# print(m.getRootHash())
print(m.getMembershipProof('duck'))
