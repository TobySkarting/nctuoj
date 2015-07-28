/* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */
/*                                 _ooOoo_                                   */
/*                                o8888888o                                  */
/*                                88" . "88                                  */
/*                                (| -_- |)                                  */
/*                                O\  =  /O                                  */
/*                             ____/`---'\____                               */
/*                           .'  \\|     |//  `.                             */
/*                          /  \\|||  :  |||//  \                            */
/*                         /  _||||| -:- |||||-  \                           */
/*                         |   | \\\  -  /// |   |                           */
/*                         | \_|  ''\---/''  |   |                           */
/*                         \  .-\__  `-`  ___/-. /                           */
/*                       ___`. .'  /--.--\  `. . __                          */
/*                    ."" '< `.___\_<|>_/___.'  >'"".                        */
/*                   | | :  `- \`.;`\ _ /`;.`/ - ` : | |                     */
/*                   \  \ `-.   \_ __\ /__ _/   .-` /  /                     */
/*              ======`-.____`-.___\_____/___.-`____.-'======                */
/*                                 `=---='                                   */
/*              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^                */
/*                       佛祖保佑       永無bug                              */
/* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */
#include "function.h"


std::string exec_path(){
    char result[PATH_MAX];
    ssize_t count = readlink("/proc/self/exe", result, PATH_MAX);
    return std::string(result, std::max(int(count), 0));
}
std::string root_dir(){
    std::string re = exec_path();
    re = re.substr(0, re.find_last_of("/"));
    re = re.substr(0, re.find_last_of("/")+1);
    return re;
}

std::string bin_dir(){
    return root_dir() + std::string("bin/");
}

std::string log_dir(){
    return root_dir() + std::string("log/");
}

std::string submission_dir_by_id(int id){
    return root_dir() + std::string("submission/") + int2string(id) + std::string("/");
}

std::string attachment_dir_by_id(int id){
    return root_dir() + std::string("attachment/") + int2string(id) + std::string("/");
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
