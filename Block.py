import MerkleTree


class Block:
    def __init__(self, prevHash: str, merkleTree: MerkleTree, nonce: int):
        self._prevHash = prevHash
        self._merkleTree = merkleTree
        self._nonce = nonce

