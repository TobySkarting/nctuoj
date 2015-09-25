#!/bin/sh
BUILD='build'
#sudo apt-get install libreadline6 libreadline6-dev 
#mkdir $BUILD
cd $BUILD
#git clone https://chromium.googlesource.com/chromium/tools/depot_tools.git
#export PATH=$PATH:`pwd`/depot_tools
#echo $PATH
#gclient
#git clone git://github.com/v8/v8.git
cd v8
#make dependencies
#make x64.release library=shared soname_version=1.0 console=readline snapshot=off werror=no
#sudo cp out/x64.release/lib.target/lib* /usr/local/lib/
#sudo cp out/x64.release/d8 /usr/local/bin/
#sudo ln -sf /usr/local/lib/libv8.so.1.0 /usr/local/lib/libv8.so
#sudo mkdir /usr/local/include/v8
sudo cp include/*.h /usr/local/include/v8/
