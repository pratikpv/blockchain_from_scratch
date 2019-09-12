import json
import random

import ECC


def getKeyAndSignature(input_text):
    G = ECC.Point(397, -2, 2, (284, 118))
    ecc = ECC.SimpleECC(G)
    signature = ecc.sign(input_text)
    return {"G": G, "pk":ecc.key(), "msg":input_text, "signature": signature}


#RSAkey.verify(hash,      signature)    # This sig will check out
#RSAkey.verify(hash[:-1], signature)    # This sig will fail

def verifySignature(G, pk, n, msg, s):
    return ECC.verify(G, pk, n, msg, s)



class DataSimulator:

    def __init__(self):
        self.timer = 0
        raw_data = open("headlinesNew.json").read()

        self.headlines = json.loads(raw_data)
        self.keys = list(self.headlines.keys())


    def getNewData(self):
        key = self.keys[self.timer]
        self.timer = min(self.timer+1, len(self.keys)-1)
        return self.headlines[key]
