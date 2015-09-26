#!/bin/sh
bash < <(curl -s -S -L https://raw.githubusercontent.com/moovweb/gvm/master/binscripts/gvm-installer)
echo "[[ -s \"$HOME/.gvm/scripts/gvm\" ]] && source \"$HOME/.gvm/scripts/gvm\"" >> $HOME/.zshrc
source $HOME/.zshrc
