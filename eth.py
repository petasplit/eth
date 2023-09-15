#!/usr/bin/env python
# coding=utf8

# Ethereum Collider
# Copyright (C) 2017  Trent Pierce
#
# Pure Python address generator with Collision detection
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>
#
# Enter optional argument : a hex string shorter than 11 chars

import hashlib
import re
import sys
import os
import time

def hexa(cha):
    hexas = hex(cha)[2:-1]
    while len(hexas) < 64:
        hexas = "0" + hexas
    return hexas

def hashrand(num):
    # Generate a pseudo-random hash based on current time
    seed = int(time.time())
    rng_data = hashlib.sha256(str(seed).encode()).hexdigest()
    for _ in range(num - 1):
        rng_data = hashlib.sha256(rng_data.encode()).hexdigest()
    return rng_data

def randomforkey():
    candint = 0
    r = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
    while candint < 1 or candint >= r:
        cand = hashrand(1024)
        candint = int(cand, 16)
    return candint

def compute_adr(priv_num):
    try:
        pubkeyhex = hexa(priv_num)
        return hashlib.sha3_256(pubkeyhex.encode()).hexdigest()[-40:]
    except KeyboardInterrupt:
        return "x"

def print_balance():
    global balance
    balance = '0'
    print('Ethereum Collider developed by Trent Pierce (www.SkeeBomb.com)')
    print()
    print('To promote development, please send donations to 01171ab97216939Ddf49b8Ac9DFFE80b8178fcF6')
    print()
    return balance

if __name__ == '__main__':
    print_balance()
    wallets = 0
    while balance == '0':
        try:
            if len(sys.argv) > 1:
                arg1 = sys.argv[1]
                assert re.match(r"^[0-9a-fA-F]{1,10}$", arg1) is not None
                searchstring = arg1.lower()
                listwide = 4 * os.cpu_count() * 2 ** len(searchstring)
                vanity = True
        except:
            raise ValueError("Error in argument, not a hex string or longer than 10 chars")
        privkeynum = randomforkey()
        address = compute_adr(privkeynum)
        foundprivkeynum = privkeynum
        if 'inter' not in locals():
            wallets = wallets + 1
            assert compute_adr(foundprivkeynum) == address
            pvhex = hexa(foundprivkeynum)
            print('\r' + 'Searched ', wallets, ' addresses')

            if balance != '0':
                print('Wallet Found!')
                print("\nAddress :  %s \n" % address)
                print("PrivKey :  %s\n" % pvhex)
                privfileexist = False
                conf = "n"
                if os.path.isfile('priv.prv'):
                    privfileexist = True
                    conf = input("Enter 'y' to confirm overwriting priv.prv file : ")
                if (conf == "y" or not privfileexist):
                    with open('priv.prv', 'w') as f:
                        f.write(pvhex)
                    print("Private key exported in priv.prv file")
                    print("Can be imported in geth : 'geth account import priv.prv'\n")
