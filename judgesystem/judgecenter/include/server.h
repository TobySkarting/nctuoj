#ifndef SERVER_H
#define SERVER_H
#include <string>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <errno.h>
#include <unistd.h>
#include <iostream>
#include <cstring>
#include <list>
#include <ctime>
#include "log.h"
#include "config.h"
#include "class_mysql.h"
#include "function.h"


#define SERVER_EXIT -1
#define SERVER_RESTART -2

#define CLIENT_TYPE_WAIT 0
#define CLIENT_TYPE_JUDGE 1
#define CLIENT_TYPE_WEB 2

#define MSG_SUCC 0
#define MSG_ERR 1

const int BUFFER_SIZE = 1024;
class SERVER{
    struct CLIENT{
        int         client_type;    //0: judge 1: web
        struct tm   last_active;
        bool        live_notify;
        int         socket;
        sockaddr_in addr;
        socklen_t   addr_len;
        std::string ip;
        bool        busy;
        int         submission_id;
        CLIENT(){
            live_notify = 0;
            client_type = CLIENT_TYPE_WAIT;
            last_active = get_nowtime();
        }
    };
    private:
		sockaddr_in m_server;
		int         m_server_socket;
		int         m_server_len;

        CONFIG          m_config;
        CLASS_MYSQL     m_mysql;
        
        std::list<int>      m_submission_list;
        std::list<CLIENT>   m_client_list;

        LOG     m_log;

        fd_set  readfd;

        void Idle_Check();
        void Get_Submission();
        void Sent_Submission();
        void Set_FD();
        void Server();
        void Client();
        int Client_Wait(std::list<CLIENT>::iterator, std::string);
        int Client_Judge(std::list<CLIENT>::iterator, std::string);
        int Client_Web(std::list<CLIENT>::iterator, std::string);
        int Command_Line();
        
    public:
        SERVER();
        ~SERVER();
        int start();
        void stop();
};

#endif
