#!/bin/zsh
cd "/Users/lukewabro/Documents/Wabro 2/WABRO"
python3 tools/wabro_hub.py --mode live-osc --rate 10 --http-port 8765 --eeg-osc-port 5002 --osc-target 127.0.0.1:9000
