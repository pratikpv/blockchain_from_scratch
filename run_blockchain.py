# CS266: Fall 2019
# HW1
#
# Pratik Prajapati
# Ashraf Saber
#

from DataSimulator import DataSimulator
import ECC
import MerkleTree as mtree
import Block as blk

# store dictionary named allValidTxList for all tx processed.
# key = hash(msg)
# value = tuple (msg, pk, signature)
allValidTxList = {}

# stock objects of class Block in ordered list
blockchain = []

# line len for pretty printing
LINE_LEN = 100


def mineGenesisBlock():
    """
    uses genesis_data as msg to mine the genesis block
    :return: Object of type Block for the genesis block and its hash
    """
    genesis_data = ['CS266: HW1 blockchain, by Pratik and Asraf']

    genesis_merkle = mtree.MerkleTree(genesis_data)
    genesis_merkle.generateTree()
    prevHash = '00000000000000000000000000000000'

    genesis_block = blk.Block(prevHash, genesis_merkle)
    genesis_hash = genesis_block.mineBlock()

    return genesis_block, genesis_hash


def run_blockchain(genesisHash: str):
    """
    Execute the blockchain, reads data from  DataSimulator() and mines the blocks for valid transactions.
    :param genesisHash: has of The Genesis Block
    :return: None
    """
    prevHash = genesisHash
    DS = DataSimulator()

    #
    # execute the loop to mine the blocks total count# of times.
    count = 6

    # Set debug = True for verbose prints
    debug = False
    while count > 0:
        newData = DS.getNewData()
        if newData is not None:
            # print newData
            count -= 1
            numberOfTx = len(newData)

            if debug:
                print('got new data of len = %d' % (numberOfTx))

            # validate each transaction
            validTxList = []
            for txIndex in range(0, numberOfTx):

                if debug:
                    print(newData[txIndex])

                # add each valid tx to validTxList, drop invalid tx
                if ECC.verify(newData[txIndex]['pk'], newData[txIndex]['msg'], newData[txIndex]['signature']):
                    if debug:
                        print("adding valid tx -> " + newData[txIndex]['msg'])
                    tx = [newData[txIndex]['msg'], newData[txIndex]['pk'], newData[txIndex]['signature']]
                    validTxList.append(tx)
                    allValidTxList[ECC.hash(str(newData[txIndex]['msg']))] = tx
                else:
                    if debug:
                        print("dropping invalid tx -> " + newData[txIndex]['msg'])

            # create merkle tree from list of valid tx
            validTxList.sort()
            if debug:
                print(validTxList)

            m = mtree.MerkleTree(validTxList)
            m.generateTree()

            # Create a block object with the merkle tree
            b = blk.Block(prevHash, m)
            # mineBlock returns hash of current block. this hash becomes prevHash for the next block
            prevHash = b.mineBlock()

            if debug:
                print('blockHash = ', prevHash, end=' ')

            b.printBlock()
            print('-' * LINE_LEN)
            # store the blocks mined with its hash
            blockchain.append(b)

        else:
            print('end of data')
            break

    if debug:
        print(allValidTxList)


def prove_data_membership(input_data: str):
    """
    - Calculate the HASH of the input_data, Gets the corresponding tuple which is (msg, pk, signature)
    - traverse the blockchain to find the block which has the data.

    :param input_data: a msg string to lookup
    :return: a Tuple of blockchain_proof, merkle_tree_proof from the block which has the data, data_tuple which is (msg, pk, signature)
            a tuple of (None, None, None) is return is data is not found.
    """
    # find data from allValidTxList that we have processed
    try:
        input_data_hash = ECC.hash(str(input_data))
        data_tuple = allValidTxList[input_data_hash]
    except KeyError:
        # we dont have this data in out blockchain
        return False, None

    hash_of_data_tuple = ECC.hash(str(data_tuple))
    blockchain_proof = []
    for b in reversed(range(len(blockchain))):
        block = blockchain[b]
        blockchain_proof.append(block)
        merkle_tree_proof = block.getProof(hash_of_data_tuple)
        if merkle_tree_proof is not None:
            # found the data
            return blockchain_proof, merkle_tree_proof, data_tuple

    return None, None, None


if __name__ == "__main__":

    # first mine The Genesis Block
    genesisBlock, genesisHash = mineGenesisBlock()
    print('=' * LINE_LEN)
    print('genesis Hash = ', genesisHash, end=' ')
    genesisBlock.printBlock()
    print('=' * LINE_LEN)

    ####################################################
    #  This is the main loop to mine all the blocks
    ####################################################
    run_blockchain(genesisHash)
    print('=' * LINE_LEN)

    # check with bad data, this is supposed to fail
    test_invalid_data = False
    if test_invalid_data:
        input_data = 'cabinet meets to balance budget priorities XXX'
        isValid, path = prove_data_membership(input_data)
        if not isValid:
            print('input_data = %s not in blockchain' % (input_data))
        else:
            print('input_data = %s in in blockchain. path ' % (path))

    # check with good data, this is supposed to pass
    input_data = 'cabinet meets to balance budget priorities'
    blockchain_proof, merkle_tree_proof, data_tuple = prove_data_membership(input_data)
    if blockchain_proof is None:
        print('Input data = %s not in blockchain' % (input_data))
    else:
        print('Input data is in blockchain. The proof is:')
        print('=' * LINE_LEN)
        print('The Blockchain: ')
        for b in range(len(blockchain_proof)):
            blockchain_proof[b].printBlock()
        print('=' * LINE_LEN)
        print('The Merkle Tree:\n' + str(merkle_tree_proof))
        # print('data_tuple : ' + str(data_tuple[0]))
        print('=' * LINE_LEN)
        print('data passed : ' + input_data)
        print('pk : ' + str(data_tuple[1]))
        print('signature : ' + str(data_tuple[2]))
        print('=' * LINE_LEN)
