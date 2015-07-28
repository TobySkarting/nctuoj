#include "config.h"

CONFIG::CONFIG(){
	std::string config_file_path = judgecenter_dir() + std::string("/config");
    std::ifstream ifs;
	ifs.open( config_file_path.c_str() );
	ifs >> m_port;
	ifs >> m_max_wait_listen;
	ifs >> m_mysql_server;
	ifs >> m_mysql_user;
	ifs >> m_mysql_password;
	ifs >> m_mysql_database;
	ifs.close();
}
CONFIG::~CONFIG(){
}
int CONFIG::port(){
	return m_port;
}
int CONFIG::max_wait_listen(){
	return m_max_wait_listen;
}
std::string CONFIG::mysql_server(){
	return m_mysql_server;
}
std::string CONFIG::mysql_user(){
	return m_mysql_user;
}
std::string CONFIG::mysql_password(){
	return m_mysql_password;
}
std::string CONFIG::mysql_database(){
	return m_mysql_database;
}
