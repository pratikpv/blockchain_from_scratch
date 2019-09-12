from DataSimulator import DataSimulator
import ECC
import MerkleTree as mtree

DS = DataSimulator()

count = 2

while count > 0:
    newData = DS.getNewData()
    if newData is not None:
        # print newData
        count -= 1
        numberOfTx = len(newData)
        print('got new data of len = %d' % (numberOfTx))
        # validate each transaction
        validTxList = []
        for txIndex in range(0, numberOfTx):
            # print (newData[txIndex])

            # add each valid tx to validTxList, drop invalid tx
            if ECC.verify(newData[txIndex]['pk'], newData[txIndex]['msg'], newData[txIndex]['signature']):
                # print ("valid")
                validTxList.append(str(newData[txIndex]['msg']))
            else:
                pass
                # print ("dropping invalid tx -> " + newData[txIndex])

        # print ("validTxList is ")
        # print (validTxList)
        # create merkel tree from validTxList
        validTxList.sort()
        m = mtree.MerkleTree(validTxList)
        m.generateTree()
        #print(m.getRootHash())
        m.postOrderPrintTree()

    else:
        print('end of data')
        break
