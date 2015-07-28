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
#ifndef JUDGE_H
#define JUDGE_H

#include <vector>
#include <string>
#include <cstring>
#include <unistd.h>
#include <sstream>
#include <iostream>

#include <sys/wait.h>
#include <sys/types.h>
#include <sys/ptrace.h>
#include <sys/time.h>
#include <sys/resource.h>

#include "config.h"
#include "class_mysql.h"
#include "function.h"
#include "log.h"
#include "ftp.h"

#define LANG_C          0
#define LANG_CPP        1
#define LANG_PYTHON2    2
#define LANG_PYTHON3    3
#define LANG_JAVA       4

struct RESULT{
    int type;
    long long time_usage;   //ms
    long long memory_usage; //kb
};

class EXECL_PAR{
    private:
        char **execl_par;
        int execl_size;
    public:
        EXECL_PAR() : execl_par(NULL), execl_size(0){}
        ~EXECL_PAR(){
            clear();
        }
        void clear(){
            for(int i = 0 ; i < execl_size ; i++)
                delete [] execl_par[i];
            delete [] execl_par;
            execl_size = 0;
        }
        char** parse(std::string command){
            std::stringstream ss(command);
            std::vector<std::string> v_str;
            std::string str;
            while(ss >> str)
                v_str.push_back(str);
            execl_size = v_str.size();
            execl_par = new char*[execl_size + 1];
            for(int i = 0 ; i < execl_size ; i++){
                execl_par[i] = new char[v_str[i].size()+1];
                strcpy(execl_par[i], v_str[i].c_str());
            }
            execl_par[execl_size] = NULL;
            return execl_par;
        }
};
/* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */ 
/* judge class will do everything about judge                            */
/* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */
class Judge{
    private:
        LOG m_log;
        CONFIG config;
        CLASS_MYSQL mysql;
        FTP ftp;
        int submission_id;
        int lang;
        int problem_id;
        int run_type_id;
        bool run_only_pri;
        std::pair<std::string, bool> run_step;
    public:
        Judge();
        ~Judge();

        /* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */ 
        /* judge function will set submission id and start to judge it           */
        /* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */
        void judge(int);

        /* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */ 
        /* get information function will                                         */
        /* get problem_id, run_type_id, run_only_pri                             */
        /* run_only_pri means that all commnad will execute for each testdata    */
        /* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */
        void get_information();

        /* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */ 
        /* get submission code function will                                     */
        /* use ftp to get submission code for this submission_id                 */
        /* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */
        bool get_submission_code();

        /* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */ 
        /* get problem attachment will                                           */
        /* use ftp and sql to get problem attachment by compiler_type            */
        /* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */
        bool get_problem_attachment();

        
        bool get_testdata(int);
        bool get_testdata_attachment(int);
};

#endif
