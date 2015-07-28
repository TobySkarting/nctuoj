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
#ifndef FUNCTION_H
#define FUNCTION_H

#include <string>
#include <limits.h>
#include <unistd.h>
#include <sstream>
#include <algorithm>

#define print_var(x) std::cout << #x << ' ' << x << std::endl


std::string exec_path();
std::string root_dir();
std::string bin_dir();
std::string log_dir();
std::string submission_dir_by_id(int);
std::string testdata_dir_by_id(int);
std::string attachment_dir_by_id(int);


int string2int(std::string);
std::string int2string(int);

#endif
