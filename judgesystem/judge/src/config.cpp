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
#include "config.h"

CONFIG::CONFIG(){
	std::string config_file_path = root_dir() + std::string("/config");
    std::ifstream ifs;
	ifs.open( config_file_path.c_str() );
    ifs >> m_ip;
	ifs >> m_port;
    ifs >> m_mysql_server;
    ifs >> m_mysql_user;
    ifs >> m_mysql_password;
    ifs >> m_mysql_database;
    ifs >> m_ftp_server;
    ifs >> m_ftp_user;
    ifs >> m_ftp_password;
	ifs.close();
}
CONFIG::~CONFIG(){
}
std::string CONFIG::ip(){
    return m_ip;
}
int CONFIG::port(){
	return m_port;
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

std::string CONFIG::ftp_server(){
    return m_ftp_server;
}
std::string CONFIG::ftp_user(){
    return m_ftp_user;
}
std::string CONFIG::ftp_password(){
    return m_ftp_password;
}
