# Sample blockchain concept implementation from scratch



## Main blockchain construction

* Implements a blockchain - in particular, a main loop that repeatedly obtains new data and computes and outputs the hash ​H(d)​ of data structure ​d​.
	* The data structure ​d​ must contain
		*  hash of the previous block
		* A Merkle Tree 
		* A nonce
		* The first 16 (binary) digits of each block hash must be 0.
	* Uses Elliptic Curve Cryptography (ECC) - (library provided)
* Implements Merkle Tree
	* The Merkle Tree must be build from all valid elements received from the
DataSimulator, i.e. all valid ​(publicKey, message, signature)​ tuples where the signature
is valid

## Provides a Merkle Tree-proof 
* A Merkle Tree-proof that a specific item is part of the Merkle Tree in an ancestor of the last block. 
* In detail, given the created blockchain after 5 blocks, shows proof that the headline <code>cabinet meets to balance budget priorities</code> was  “put on the blockchain.”

Sample output:

<!-- language: lang-none -->

    $ python3 run_blockchain.py 
	================================================================================
	genesis Hash =  0000c3cb141422f9736ff35e5fdda5a3 prevHash = 00000000000000000000000000000000 merkleTree-root = 1b31113d4865b2f04b82802702a7c555 nonce = 38032
	================================================================================
	prevHash = 0000c3cb141422f9736ff35e5fdda5a3 merkleTree-root = 881f2b580cb3db870f86eebbf67c7f0b nonce = 48348
	--------------------------------------------------------------------------------
	prevHash = 0000dd87ad348f335b2bd4957940d696 merkleTree-root = c0ca1303491a3c9346647fe90ba84adc nonce = 34893
	--------------------------------------------------------------------------------
	prevHash = 0000fec3ba530b2276e45a5a8c8b169f merkleTree-root = ccb7b3fc9646e62d46868481e105b97b nonce = 25596
	--------------------------------------------------------------------------------
	prevHash = 000064cd652e7633581b3fb2fcbd5e31 merkleTree-root = 0286ffabfb1af0184d7b8ab0637b748a nonce = 90084
	--------------------------------------------------------------------------------
	prevHash = 0000c33e9c69a46ddd8e4d1d65907b9b merkleTree-root = bee46a181a71875222bd87eb65aed5ad nonce = 21758
	--------------------------------------------------------------------------------
	prevHash = 0000066320056b688dc7a2048a6ea00d merkleTree-root = 662bd1be5c6c876be3c7a4373202c45b nonce = 23624
	--------------------------------------------------------------------------------
	================================================================================
	Input data is in blockchain. The proof is:
	================================================================================
	The Blockchain: 
	prevHash = 0000066320056b688dc7a2048a6ea00d merkleTree-root = 662bd1be5c6c876be3c7a4373202c45b nonce = 23624
	prevHash = 0000c33e9c69a46ddd8e4d1d65907b9b merkleTree-root = bee46a181a71875222bd87eb65aed5ad nonce = 21758
	prevHash = 000064cd652e7633581b3fb2fcbd5e31 merkleTree-root = 0286ffabfb1af0184d7b8ab0637b748a nonce = 90084
	prevHash = 0000fec3ba530b2276e45a5a8c8b169f merkleTree-root = ccb7b3fc9646e62d46868481e105b97b nonce = 25596
	prevHash = 0000dd87ad348f335b2bd4957940d696 merkleTree-root = c0ca1303491a3c9346647fe90ba84adc nonce = 34893
	prevHash = 0000c3cb141422f9736ff35e5fdda5a3 merkleTree-root = 881f2b580cb3db870f86eebbf67c7f0b nonce = 48348
	================================================================================
	The Merkle Tree:
	['881f2b580cb3db870f86eebbf67c7f0b', ['50b2fea9c695ad3927c5d1ac9331e963', ['c6308ce9c86597433b32464caadf5ea9', ['c56ac8c18428001ef049ed89bc604294', ['41c7a37357742592479c9aa95248f166', 'b6ea3525b95676f488b8f1c6dff8848d']]]], '461e9d8a9d2021f13e840fbbfee46fd5']
	================================================================================
	data passed : cabinet meets to balance budget priorities
	pk : Curve( 463 -2 2 ); G( 155 452 ); PK( 263 231 ); PKOrder( 149 )
	signature : [9, 30]
	================================================================================

