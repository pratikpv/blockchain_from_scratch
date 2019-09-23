from DataSimulator import DataSimulator
import ECC
import MerkleTree as mtree

# data_list = ['alice', 'carol', 'duck', 'bob']

#data_list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
data_list = ['a', 'b', 'c', 'd', 'e', 'f']
m = mtree.MerkleTree(data_list)
m.generateTree()
m.postOrderPrintTree()
# print(m.getRootHash())
data = ECC.hash('a')
path = m.getMembershipProof(data)
if path is not None:
    print(' path = ' + str(path))
else:
    print(' membership failed')
