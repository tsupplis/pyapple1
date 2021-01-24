#!/usr/bin/env python3

import Memory
import PIA6821
import Terminal
import Processor

import argparse
import threading
import os

dir_path = os.path.dirname(os.path.realpath(__file__))

parser = argparse.ArgumentParser(description="Apple 1 Emulator")
parser.add_argument("-m", "--model",
        help="set model to apple1 (default) or replica1",
        default="apple1")
parser.add_argument("-l", "--load",
        help="load program at 0x280",
        default=None)
parser.add_argument("-w", "--writerom",
        help="allow writes to ROM (default: false)", 
        type=bool, default=False)
parser.add_argument("-r", "--ramsize",
        help="set ram size in KB (default: 4 KB for apple1, 32 KB for replica1)",
        type=int, default=0)

args = parser.parse_args()

decoder = Memory.Decoder()

processor = Processor.Processor(decoder)

# default options for an apple 1
ramsize = 4 * 1024
rompath = "roms/wozmon.bin"
rombase = 0xff00
romsize = 0x100

if args.model == "apple1":
    ramsize = 4 * 1024
    rompath = dir_path+"/roms/wozmon.bin"
    rombase = 0xff00
    romsize = 0x100

elif args.model == "replica1":
    ramsize = 32 * 1024
    rompath = dir_path+"/roms/replica1.bin"
    rombase = 0xe000
    romsize = 0x2000
elif args.model == "applesoft":
    ramsize = 32 * 1024
    rompath = dir_path+"/roms/applesoft.bin"
    rombase = 0xe000
    romsize = 0x2000
else:
	args.model= "unkown"

if args.ramsize != 0:
    ramsize = args.ramsize * 1024

print ("Apple 1 Simulator");
print ("Ram Size : ", ramsize)
print ("Model    : ", args.model)

ram = Memory.RAM(decoder, 0, ramsize) 
rom = Memory.ROM(decoder, rombase, romsize)
rom.load(open(rompath, "rb"))

if args.load != None:
    f=open(args.load,"rb");
    for i in range(0, os.fstat(f.fileno()).st_size):
        t = f.read(1)
        if t == b'':
            t = 0
        else:
            t = ord(t)
        ram[i+0x280] = t



terminal = Terminal.Terminal(processor)

pia = PIA6821.PIA6821(decoder, terminal)

termthread = threading.Thread(target=terminal.run)
procthread = threading.Thread(target=processor.run)

procthread.daemon = True

termthread.start()
procthread.start()
