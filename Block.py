# CS266: Fall 2019
# HW1
#
# Pratik Prajapati
# Ashraf Saber
#

import MerkleTree
import ECC


class Block:
    """
    This class represents the block, with prevHash, merkleTree and nonce
    nonce would be mined by calling mineBlock() method.
    preset variable in isHashInTarget represents numver of binary digits to be zero for the target hash.
    """

    def __init__(self, prevHash: str, merkleTree: MerkleTree):
        self._prevHash = prevHash
        self._merkleTree = merkleTree
        self._nonce = None

    def getMerkleTree(self):
        """
        get Hash of current block
        """
        if not isinstance(self._merkleTree, MerkleTree.MerkleTree):
            return None

        return self._merkleTree

    def getPrevHash(self):
        return self._prevHash

    def getNonce(self):
        return self._nonce

    def getMerkleTree(self):
        return self._merkleTree

    def isHashInTarget(self, hash):
        """
        The first 16 (binary) digits of each block hash must be 0.
        """
        preset = 16
        # devide preset by 4 as each hex number represents 4 bits
        numOfZero = int(preset / 4)

        if str(hash).startswith('0' * numOfZero):
            return True

        return False

    def mineBlock(self):

        self._nonce = 0
        while True:
            newHash = ECC.hash(str(self._prevHash) + str(self._nonce) + str(self.getMerkleTree().getRootHash()))
            if self.isHashInTarget(newHash):
                return newHash
            else:
                self._nonce += 1

    def printBlock(self):
        print('prevHash = %s merkleTree-root = %s nonce = %d' % (
            self.getPrevHash(), self.getMerkleTree().getRootHash(), self.getNonce()))

    def getProof(self, data):
        # get membership proof of the data in the merkle tree
        path = self._merkleTree.getMembershipProof(data)
        return path
