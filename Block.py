import MerkleTree
import ECC


class Block:

    def __init__(self, prevHash: str, merkleTree: MerkleTree):
        self._prevHash = prevHash
        self._merkleTree = merkleTree
        self._nonce = None

    def getMerkleTree(self):
        """ get Hash of current block """
        if not isinstance(self._merkleTree, MerkleTree.MerkleTree):
            return None

        return self._merkleTree

    def getPrevHash(self):
        return self._prevHash

    def getNonce(self):
        return self._nonce

    def isHashInTarget(self, hash):
        """The first 16 (binary) digits of each block hash must be 0."""
        preset = 16
        # devide preset by 4 as each hex number represents 4 bits
        numOfZero = int(preset / 4)

        # method 1
        # intHash = int(hash, 16);
        # print(' hex = %s int = %d ' % (hash, intHash))
        # if int(intHash) >> (int.bit_length(intHash) - preset):
        #    return False
        # else:
        # return True

        # method 2

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

            # print values every 10x nonce tried, for debugging only
            if not (self._nonce % 1000000):
                print('newHash = %s nonce = %d ' % (newHash, self._nonce))

    def printBlock(self):
        print('prevHash = %s merkleTree-root = %s nonce = %d' % (
            self.getPrevHash(), self.getMerkleTree().getRootHash(), self.getNonce()))

    def validateBlock(self, hash):

        """ TODO how to really validate a block ? """
        newHash = ECC.hash(str(self.getNonce()) + str(hash))
        if self.isHashInTarget(newHash):
            return True, newHash

        # return False with invalid hash
        return False, -1
