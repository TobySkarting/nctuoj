sudo apt-get -y install build-essential curl git wget python3 python3-pip postgresql-server-dev-all redis-server postgresql-client
sudo pip3 install --upgrade pip
pip3 pinstall -r requirements.txt
git submodule init
git submodule sync
git submodule update
cd ./http/pdf.js
npm install
node make generic

