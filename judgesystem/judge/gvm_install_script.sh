#!/bin/sh
curl -s -S -L https://raw.githubusercontent.com/moovweb/gvm/master/binscripts/gvm-installer | bash
echo "[[ -s \"$HOME/.gvm/scripts/gvm\" ]] && source \"$HOME/.gvm/scripts/gvm\"" >> $HOME/.zshrc
echo "gvm use go1.5" >> ~/.zshrc
source $HOME/.zshrc
gvm install go1.4
gvm use go1.4
export GOROOT_BOOTSTRAP=$GOROOT
gvm install go1.5
gvm use go1.5
gvm use go1.5
