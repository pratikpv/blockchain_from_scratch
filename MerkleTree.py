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

    def _utilGetMembershipProof(self, root, path, data, level):

        if not root:
            return False

        end_marker = 'end'

        level += 1
        path[level] = [root.data, root.left.data if root.left is not None else end_marker,
                       root.right.data if root.right is not None else end_marker]
        if root.data == data:
            # we have found the data, now post process the path to generate all needed branches
            # revalidate to make sure

            #print('final path so far', path)

            if path[level][1] != end_marker:
                return False

            #level -= 1
            #data_list = path[level]
            #print('patching level data ', data_list)
            #data_list[data_list.index(data)] = 'hash of data'
            #print('patching level data now', data_list)
            for l in reversed(range(1, level)):
                #print('patching level ', l)
                data_list = path[l]
                root_of_current_level = data_list[0]
                new_data = [data_list[1], data_list[2]]
                # replace node from above level while value matches with root_of_current_level value
                data_list_above = path[l-1]
                data_list_above[data_list_above.index(root_of_current_level)] = new_data

            return True
        if self._utilGetMembershipProof(root.left, path, data, level) or self._utilGetMembershipProof(root.right, path,
                                                                                                      data, level):
            return True

        return False

    def getMembershipProof(self, data):

        if self._root is None:
            return
        # path from root to the node which contains the data.
        path = {}
        if self._utilGetMembershipProof(self._root, path, data, -1):
            processed_path = path.get(0)
            #print('final path patched', processed_path)
            return processed_path
        else:
            return None
