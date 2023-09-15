#!/usr/bin/env python3
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

import hashlib
import re
import sys
import os
import threading
import secrets

def hexa(cha):
    hexas = hex(cha)[2:-1]
    while len(hexas) < 64:
        hexas = "0" + hexas
    return hexas

def randomforkey():
    candint = 0
    r = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
    while candint < 1 or candint >= r:
        cand = secrets.randbits(256)
        candint = cand
    return candint

def compute_adr(priv_num):
    pubkeyhex = hexa(priv_num)
    return hashlib.sha3_256(pubkeyhex.encode()).hexdigest()[-40:]

def create_rainbow_table(num_addresses):
    rainbow_table = set()
    for _ in range(num_addresses):
        privkeynum = randomforkey()
        address = compute_adr(privkeynum)
        rainbow_table.add(address)
    return rainbow_table

def search_for_collision(target_address, rainbow_table):
    wallets = 0
    collision_found = False

    while not collision_found:
        privkeynum = randomforkey()
        address = compute_adr(privkeynum)

        if address in rainbow_table:
            collision_found = True
        else:
            wallets += 1

        if wallets % 1000 == 0:
            print('\r' + 'Searched ', wallets, ' addresses', end='', flush=True)

    print('Wallet Found!')
    print("\nAddress :  %s \n" % address)
    print("PrivKey :  %s\n" % hexa(privkeynum))

if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg1 = sys.argv[1]
        assert re.match(r"^[0-9a-fA-F]{1,10}$", arg1) is not None
        searchstring = arg1.lower()
        listwide = 4 * os.cpu_count() * 2 ** len(searchstring)
        vanity = True
    else:
        print("Please specify a target address as an argument.")
        sys.exit(1)

    num_addresses = 1000000  # Adjust this number to increase the chances of collision
    rainbow_table = create_rainbow_table(num_addresses)
    search_for_collision(searchstring, rainbow_table)
