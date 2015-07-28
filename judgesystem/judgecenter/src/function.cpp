#include "function.h"


std::string exec_path(){
    char result[PATH_MAX];
    ssize_t count = readlink("/proc/self/exe", result, PATH_MAX);
    return std::string(result, std::max(int(count), 0));
}
std::string judgecenter_dir(){
    std::string re = exec_path();
    re = re.substr(0, re.find_last_of("/"));
    re = re.substr(0, re.find_last_of("/")+1);
    return re;
}

int string2int(std::string str){
    std::stringstream ss(str);
    int re;
    ss >> re;
    return re;
}

std::string int2string(int x){
    std::stringstream ss;
    ss << x;
    std::string re;
    ss >> re;
    return re;
}


struct tm get_nowtime(){
    time_t now;
    time(&now);
    return *localtime(&now);
}
