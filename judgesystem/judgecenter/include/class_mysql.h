#ifndef CLASS_MYSQL_H
#define CLASS_MYSQL_H
#include <string>
#include <vector>
#include <cstdlib>
#include <unordered_map>
#include <algorithm>
#include <sstream>
#include "log.h"
#include "mysql.h"

#include <iostream>

class CLASS_MYSQL_ROW;
typedef std::vector<CLASS_MYSQL_ROW> CLASS_MYSQL_RES;
class CLASS_MYSQL;

class CLASS_MYSQL_ROW : public std::vector<std::string>{
    private:
        std::vector<std::string> col;
    public:
        void				push_back(const std::string col_name, const std::string value);
        std::string         operator[](const int pos) const;
        std::string         operator[](const std::string col_name) const;
};
class CLASS_MYSQL{
    private:
        MYSQL		m_connection;
        std::string m_server;
        std::string m_user;
        std::string m_password;
        std::string m_database;
        std::string m_mysql_log;
        LOG         m_log;
        void connect();
        void close();
        void log_info();
    public:
        CLASS_MYSQL();
        CLASS_MYSQL(const std::string, const std::string, const std::string, const std::string, const std::string _mysql_log="./mysql.log");	//set(HOST, USER, PASSWD, DB, log)
        ~CLASS_MYSQL();
        CLASS_MYSQL_RES query(const std::string);
        bool test();
};
#endif 
