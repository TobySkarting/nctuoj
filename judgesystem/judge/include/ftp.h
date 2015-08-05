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
#ifndef FTP_H
#define FTP_h

#include <string>
#include <iostream>
#include "log.h"

class FTP{
    private:
        std::string m_server;
        std::string m_user;
        std::string m_password;
        LOG m_log;
    public:
        FTP();
        FTP(std::string, std::string, std::string, std::string _ftp_log = "./ftp.log");
        bool get(std::string, std::string);
        bool put(std::string, std::string);
        /* sshpass -p vuvsawkArnErcecs scp nctuojftp@140.113.194.120:~/nctuoj_develop/data/submission/1/test.cpp  ./testgg.cpp */
        /* string("curl -s --create-dirs -u ") + config.ftp_user() + string(":") + config.ftp_password() + string(" ") + source + string(" -o ") + output; */
};

#endif
