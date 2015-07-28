#include "server.h"
using namespace std;

int main(){
    int re = 0;
    while(re != SERVER_EXIT){
        SERVER server;
        re = server.start();
    }
}
