# CS266: Fall 2019
# HW1
#
# Pratik Prajapati
# Ashraf Saber
#

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
        """
        Generates the Merkle tree from the data
        :return: root of the tree, hash of the root node
        """
        txLen = len(self._txList)

        if txLen == 0:
            return None

        # if the number of tx is not even
        if txLen % 2 != 0:
            self._txList.append('')
            txLen += 1

        self._root, self._root.data = self._utilGenerateTree(0, txLen - 1)
        return self._root, self._root.data

    def _utilGenerateTree(self, posLeft: int, posRight: int):
        """
        utility function called by generateTree
        """
        if int(posLeft) == int(posRight):
            # if we are at a leaf
            node = Tree()
            node.data = str(ECC.hash(str(self._txList[int(posLeft)])))
            return node, node.data

        centerElement = int((posLeft + posRight) / 2)
        root = Tree()
        leftNode, leftHash = self._utilGenerateTree(posLeft, centerElement)
        rightNode, rightHash = self._utilGenerateTree(centerElement + 1, posRight)
        root.left = leftNode
        root.right = rightNode
        root.data = str(ECC.hash(str(leftHash) + str(rightHash)))

        return root, root.data

    def getRootHash(self):
        if self._root is None:
            return
        return self._root.data

    def _utilpostOrderPrintTree(self, root: Tree):
        """
        utility function called by postOrderPrintTree
        """
        if root is None:
            return

        self._utilpostOrderPrintTree(root.left)
        self._utilpostOrderPrintTree(root.right)
        print(root.data)

    def postOrderPrintTree(self):
        """
        print the tree in post order manner for debugging
        :return: None
        """
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
            # re-validate to make sure

            # print('final path so far', path)

            if path[level][1] != end_marker:
                return False

            # at leaf level replace hash of data with string 'hash of data'
            #
            # level -= 1
            # data_list = path[level]
            # data_list[data_list.index(data)] = 'hash of data'
            # path[level] = data_list
            # level += 1

            # start patching whole tree
            for l in reversed(range(1, level)):
                # print('patching level ', l)
                data_list = path[l]
                root_of_current_level = data_list[0]
                new_data = [data_list[1], data_list[2]]
                # replace node from above level while value matches with root_of_current_level value
                data_list_above = path[l - 1]
                data_list_above[data_list_above.index(root_of_current_level)] = new_data

            return True
        if self._utilGetMembershipProof(root.left, path, data, level) or self._utilGetMembershipProof(root.right, path,
                                                                                                      data, level):
            return True

        return False

    def getMembershipProof(self, data):
        """
         get merkle tree proof of the given data
        :param data: hash to look up
        :return: list of the list for the merkle tree proof. sub list represents the sub tree
        """
        if self._root is None:
            return None
        # path from root to the node which contains the data.
        path = {}
        if self._utilGetMembershipProof(self._root, path, data, -1):
            processed_path = path.get(0)
            # print('final path patched', processed_path)
            return processed_path
        else:
            return None

    def _reduce(self, path: list):
        """
        the path would be list of lists, reduce the path to single element by hashing each element of list
        :param path:
        :return: root hash
        """
        sumValues = ""
        for index in range(len(path)):
            if type(path[index]) == list:
                sumValues += str(self._reduce(path[index]))
                sumValues = ECC.hash(str(sumValues))
            else:
                sumValues += str(path[index])
        return sumValues

    def validateProof(self, data_path: list):
        """
        validate proof generated by getMembershipProof()
        :param data_path:
        :return: True if proof passed is valid, else False
        """
        if type(data_path) != list:
            return False

        # make a copy, so that we dont modify the input
        path = data_path[:]
        reduced_path = [path[0], self._reduce(path.pop(0))]
        return True if reduced_path[0] == reduced_path[1] else False

    def _utilgetLabledProof(self, lst: list, final_op, data):

        for x in range(len(lst)):
            if isinstance(lst[x], list):
                if x % 2:
                    return ' right = [' + self._utilgetLabledProof(lst[x], final_op, data) + ']'
                else:
                    return ' left = [' + self._utilgetLabledProof(lst[x], final_op, data) + ']'
            else:
                if x % 2:
                    print('at right ' + str(lst[x]))
                    final_op += ' right = [' + str(lst[x]) + ']'
                else:
                    print('at left ' + str(lst[x]))
                    final_op += ' left = [' + str(lst[x]) + ']'
        return final_op

    def getLabledProof(self, data):
        data_proof = self.getMembershipProof(data)
        if data_proof is None:
            return None

        data_proof_temp = data_proof[1:]
        final_op = ''
        final_op = self._utilgetLabledProof(data_proof_temp, final_op, data)
        final_op = 'root = ' + str(data_proof[0]) + final_op
        # print(final_op)
        return final_op

    def _utilprintLabeledProof(self, lst: list):
        y = ''
        for x in range(len(lst)):
            if x == 0:
                y = 'left= '
            elif x == 1:
                y = 'right= '
            if type(lst[x]) == list:
                y += str(lst[x])
                print(str(y))
                y = ""
                self._utilprintLabeledProof(lst[x])
            else:
                print(str(y) + str(lst[x]))
                y += str(lst[x])
                y = ''

        return y

    def printLabeledProof(self, data):
        path = self.getMembershipProof(data)
        if path is None:
            return None
        path.pop(0)
        y = self._utilprintLabeledProof(path)
        return y
