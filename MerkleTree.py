import ECC


class Tree:
    """
    data is hash value if left and right is not null(None) -> non leaf nodes
    data is tx data  if left and right are null(None) -> leaf nodes
    """

    def __init__(self):
        self.left = None
        self.right = None
        self.data = None


class MerkleTree:

    def __init__(self, txList):
        self._txList = txList
        self._root = None

    def generateTree(self):

        txLen = len(self._txList)

        if txLen == 0:
            return None

        # if the number of tx is not even
        if txLen % 2 != 0:
            self._txList.append('')
            txLen += 1

        # print(' passed list' + str(self._txList) + ' len ' + str(txLen))
        self._root, self._root.data = self._utilGenerateTree(0, txLen - 1)
        return self._root, self._root.data

    def _utilGenerateTree(self, posLeft: int, posRight: int):

        # print('left ' + str(posLeft) + ' right ' + str(posRight))
        if int(posLeft) == int(posRight):
            # if we are at a leaf
            node = Tree()
            node.data = str(ECC.hash(str(self._txList[int(posLeft)])))
            # print(' leaf data ' + node.data + ' hash ' + ECC.hash(node.data))
            return node, node.data

        centerElement = int((posLeft + posRight) / 2)
        root = Tree()
        leftNode, leftHash = self._utilGenerateTree(posLeft, centerElement)
        rightNode, rightHash = self._utilGenerateTree(centerElement + 1, posRight)
        root.left = leftNode
        root.right = rightNode
        root.data = str(ECC.hash(str(leftHash) + str(rightHash)))

        # print(' root data ' + root.data + ' hash ' + ECC.hash(root.data) + ' left ' + leftHash
        #      + ' right ' + rightHash)
        return root, root.data

    def getRootHash(self):
        if self._root is None:
            return
        return self._root.data

    def _utilpostOrderPrintTree(self, root: Tree):

        if root is None:
            return

        self._utilpostOrderPrintTree(root.left)
        self._utilpostOrderPrintTree(root.right)
        print('data ' + root.data)

    def postOrderPrintTree(self):

        if self._root is None:
            return

        if not isinstance(self._root, Tree):
            print('invalid root passed')
            return
        self._utilpostOrderPrintTree(self._root)

    def _utilGetMembershipProof(self, root, path, data):

        if not root:
            return False

        path.append(root.data)
        if root.data == data:
            return True
        if self._utilGetMembershipProof(root.left, path, data) or self._utilGetMembershipProof(root.right, path, data):
            return True
        path.pop(-1)

        return False

    def getMembershipProof(self, data):

        if self._root is None:
            return
        # path from root to the node which contains the data.
        path = []
        if self._utilGetMembershipProof(self._root, path, data):
            return path
        else:
            return None
