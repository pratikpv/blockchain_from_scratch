# The data is provided via a class DataSimulator

import DataSimulator as DSim

DS = DSim.DataSimulator()

count  = 10

while count > 0:
    newData = DS.getNewData()
    if newData is not None:
        print 'got data -------------\n'
        print newData
        count -=1
    else:
        print 'end of data'
        break