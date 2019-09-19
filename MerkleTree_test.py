from DataSimulator import DataSimulator
import ECC
import MerkleTree as mtree

data_list = ['alice', 'carol', 'duck', 'bob']

#data_list.sort()
m = mtree.MerkleTree(data_list)
m.generateTree()
m.postOrderPrintTree()
# print(m.getRootHash())
data = ECC.hash('alice')
path = m.getMembershipProof(data)
if path is not None:
    print(' path = ' + str(path))
else:
    print(' membership failed')
