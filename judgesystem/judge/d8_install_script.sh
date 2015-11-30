#!/bin/sh
BUILD='build'
sudo apt-get install libreadline6 libreadline6-dev 
mkdir $BUILD
cd $BUILD
git clone https://chromium.googlesource.com/chromium/tools/depot_tools.git
export PATH=$PATH:`pwd`/depot_tools
echo $PATH
fetch v8
gclient sync
make native -j 4 library=shared
sudo cp out/native/d8 /usr/local/bin/
