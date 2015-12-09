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
cd v8
make native -j 4 library=shared
sudo cp out/native/d8 /usr/local/bin/
sudo cp out/native/*.bin /usr/local/bin/
sudo cp out/native/lib.target/* /usr/local/lib
sudo cp out/native/lib.target/* /usr/lib
