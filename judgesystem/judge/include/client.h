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
#ifndef CLIENT_H
#define CLIENT_H

#include <string>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <unistd.h>
#include <iostream>
#include <cstring>

#include "config.h"
#include "log.h"
#include "function.h"


#define SOCKET_INIT_SUCC 0
#define SOCKET_INIT_ERROR 1

#define SOCKET_CONNECT_SUCC 0
#define SOCKET_CONNECT_ERROR 1


#define SERVER_CLOSE -1
#define CLIENT_CLOSE -2



const int BUFFER_SIZE = 1024;
class CLIENT{
    private:
        LOG m_log;
        CONFIG m_config;

        int m_sock;
        std::string m_server_ip;
        int m_server_port;

        sockaddr_in m_server;

        fd_set readfd;

        void SET_FD();
        int COMMAND_LINE();
        int SOCK();

    public:
        ~CLIENT();
        int INIT();
        int CONNECT();
        void CLOSE();
        int GETSUBMISSION();
        void JUDGE_DONE();

};

#endif
