from DataSimulator import DataSimulator
import ECC
import MerkleTree as mtree
import Block as blk

# store hash(data) : tuple (data, sign, pk) as dictionary for all tx processed.
allValidTxList = {}
blockchain = {}


def mineGenesisBlock():
    genesis_data = ['pratik_blockchain']

    genesis_merkle = mtree.MerkleTree(genesis_data)
    genesis_merkle.generateTree()
    prevHash = '00000000000000000000000000000000'

    genesis_block = blk.Block(prevHash, genesis_merkle)
    genesis_hash = genesis_block.mineBlock()
    # print('mined genesis_hash = %s' % (genesis_hash))

    isValid = genesis_block.validateBlock(genesis_hash)
    """
    if isValid:
        print('mined genesis_nonce is valid')
    else:
        print('mined genesis_nonce is not valid')
    """
    return genesis_block, genesis_hash


def run_blockchain(genesisHash: str):
    prevHash = genesisHash
    DS = DataSimulator()

    count = 6

    while count > 0:
        newData = DS.getNewData()
        if newData is not None:
            # print newData
            count -= 1
            numberOfTx = len(newData)
            # print('got new data of len = %d' % (numberOfTx))
            # validate each transaction
            validTxList = []
            for txIndex in range(0, numberOfTx):
                # print (newData[txIndex])

                # add each valid tx to validTxList, drop invalid tx
                if ECC.verify(newData[txIndex]['pk'], newData[txIndex]['msg'], newData[txIndex]['signature']):
                    # print ("valid")
                    # print("adding valid tx -> " + newData[txIndex]['msg'])
                    validTxList.append(str(newData[txIndex]))
                    allValidTxList[ECC.hash(str(newData[txIndex]['msg']))] = str(newData[txIndex])

            else:
                pass
                # print("dropping invalid tx -> " + newData[txIndex]['msg'])

            # create merkle tree from list of valid tx
            validTxList.sort()
            # print(validTxList)

            m = mtree.MerkleTree(validTxList)
            m.generateTree()
            b = blk.Block(prevHash, m)
            # mineBlock returns hash of current block. this hash becomes prevHash for the next block
            prevHash = b.mineBlock()
            print('blockHash = ', prevHash, end=' ')
            b.printBlock()

            # store the blocks mined with its hash
            blockchain[prevHash] = b

        else:
            print('end of data')
            break

    # print(allValidTxList)


def prove_data_membership(input_data: str):
    # find data from allValidTxList that we have processed
    try:
        input_data_hash = ECC.hash(str(input_data))
        data_tuple = allValidTxList[input_data_hash]
    except KeyError:
        return False, None

    hash_of_data_tuple = ECC.hash(str(data_tuple))
    for key in blockchain:
        block = blockchain[key]
        # TODO
        # 1. getMembershipProof should return all valid nodes
        # 2. print hash of blocks also as proof.
        path = block.getMerkleTree().getMembershipProof(hash_of_data_tuple)
        if path is not None:
            print('found data in merkle tree = %s on block = %s' % (block.getMerkleTree().getRootHash(), block))
            return True, path

    return False, None


if __name__ == "__main__":
    genesisBlock, genesisHash = mineGenesisBlock()
    print('genesis Hash = ', genesisHash, end=' ')
    genesisBlock.printBlock()

    run_blockchain(genesisHash)

    # check with bad data, this is supposed to fail
    input_data = 'cabinet meets to balance budget priorities XXX'
    isValid, path = prove_data_membership(input_data)
    if not isValid:
        print('input_data = %s not in blockchain' % (input_data))
    else:
        print('input_data = %s in in blockchain. path ' % (path))

    # check with good data, this is supposed to pass
    input_data = 'cabinet meets to balance budget priorities'
    isValid, path = prove_data_membership(input_data)
    if not isValid:
        print('input_data = %s not in blockchain' % (input_data))
    else:
        print('input_data is in blockchain -> path %s' % (path))
