#!/usr/bin/env python

import time
from hashlib import sha256

VERSION    = '01000000'.decode('hex')
PREVBLOCK  = '00'.decode('hex') * 32
MERKLEROOT = 'bdc8f49a91a4535a15f76b486cc9fe0d70bdaa8812f58ce80ba41e97aa1b3bf5'.decode('hex')
DIFFICULTY = 'ffff001d'.decode('hex')

def block_hash(epoch, nonce):
  epoch = hex(epoch)[2:].decode('hex')[::-1]
  nonce    = hex(nonce)[2:]
  nonce    = '0'*(8-len(nonce)) + nonce
  nonce    = nonce.decode('hex')[::-1]
  return sha256(sha256(VERSION + PREVBLOCK + MERKLEROOT + epoch + DIFFICULTY + nonce).digest()).digest()

epoch = int(time.time())
nonce    = 0
print "Starting at epoch %d and nonce %d" % (epoch, nonce)
while block_hash(epoch, nonce)[-4:] != '\x00\x00\x00\x00':
  nonce = nonce+1
  if nonce > 4294967295:
    epoch, nonce = epoch+1, 0
    print "Advancing to epoch %d and nonce %d" % (epoch, nonce)
  elif 0 == (nonce%100000):
    print nonce

print 'Found block!'
print "EPOCH: %d" % epoch
print "NONCE:    %d" % nonce
print "HASH:     %s" % block_hash(epoch, nonce)[::-1].encode('hex')

"""
01000000 - version
0000000000000000000000000000000000000000000000000000000000000000 - prev block
3BA3EDFD7A7B12B27AC72C3E67768F617FC81BC3888A51323A9FB8AA4B1E5E4A - merkle root
29AB5F49 - timestamp
FFFF001D - bits
1DAC2B7C - nonce
01 - number of transactions
01000000 - version
01 - input
0000000000000000000000000000000000000000000000000000000000000000FFFFFFFF - prev output
4D - script length
04FFFF001D0104455468652054696D65732030332F4A616E2F32303039204368616E63656C6C6F72206F6E206272696E6B206F66207365636F6E64206261696C6F757420666F722062616E6B73 - scriptsig
FFFFFFFF - sequence
01 - outputs
00F2052A01000000 - 50 BTC
43 - pk_script length
4104678AFDB0FE5548271967F1A67130B7105CD6A828E03909A67962E0EA1F61DEB649F6BC3F4CEF38C4F35504E51EC112DE5C384DF7BA0B8D578A4C702B6BF11D5FAC - pk_script
00000000 - lock time
"""
