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
#ifndef CONFIG_H
#define CONFIG_H
#include <string>
#include <fstream>
#include "function.h"

#define VERSION std::string("2015/06/27_01:10")

#define DEVELOP_MODE

class CONFIG{
    private:
        std::string m_ip;
        int m_port;

        std::string m_mysql_server;
        std::string m_mysql_user;
        std::string m_mysql_password;
        std::string m_mysql_database;

        std::string m_ftp_server;
        std::string m_ftp_user;
        std::string m_ftp_password;
        
    public:
        CONFIG();
        ~CONFIG();
        void init();
        std::string ip();
        int port();

        std::string mysql_server();
        std::string mysql_user();
        std::string mysql_password();
        std::string mysql_database();

        std::string ftp_server();
        std::string ftp_user();
        std::string ftp_password();
};
#endif
