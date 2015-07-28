#ifndef CONFIG_H
#define CONFIG_H
#include <string>
#include <fstream>
#include "function.h"

#define VERSION std::string("2015/06/27_01:10")

class CONFIG{
    private:
        int m_port;
        int m_max_wait_listen;
        std::string m_mysql_server;
        std::string m_mysql_user;
        std::string m_mysql_password;
        std::string m_mysql_database;
    public:
        CONFIG();
        ~CONFIG();
        void init();
        int port();
        int max_wait_listen();

        std::string mysql_server();
        std::string mysql_user();
        std::string mysql_password();
        std::string mysql_database();
};
#endif
