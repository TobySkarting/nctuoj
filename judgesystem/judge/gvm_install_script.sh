#!/bin/sh
curl -s -S -L https://raw.githubusercontent.com/moovweb/gvm/master/binscripts/gvm-installer | bash
echo "[[ -s \"$HOME/.gvm/scripts/gvm\" ]] && source \"$HOME/.gvm/scripts/gvm\"" >> $HOME/.zshrc
source $HOME/.zshrc
