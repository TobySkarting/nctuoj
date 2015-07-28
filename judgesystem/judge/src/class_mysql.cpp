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
#include "class_mysql.h"

/* ======= CLASS_MYSQL_ROW ======= */

void CLASS_MYSQL_ROW::push_back(const std::string col_name, const std::string value){
    std::vector<std::string>::push_back(value);
    col.push_back(col_name);
}
std::string CLASS_MYSQL_ROW::operator[](const int pos) const {
    return std::vector<std::string>::operator[](pos);
}
std::string CLASS_MYSQL_ROW::operator[](const std::string str) const {
    for(int i = 0 ; i < (int)col.size() ; i++)
        if(col[i] == str)
            return std::vector<std::string>::operator[](i);
    return "Invalid column name";
}
/* ======= CLASS_MYSQL ======= */

CLASS_MYSQL::CLASS_MYSQL(){
}
CLASS_MYSQL::CLASS_MYSQL(const std::string _mysql_server, const std::string _mysql_user, const std::string _mysql_password, const std::string _mysql_database, const std::string _mysql_log){
    m_server	= _mysql_server;
    m_user		= _mysql_user;
    m_password	= _mysql_password;
    m_database	= _mysql_database;
    m_mysql_log = _mysql_log;
    m_log = LOG(m_mysql_log, "MySQL");
}

CLASS_MYSQL::~CLASS_MYSQL(){
}

void CLASS_MYSQL::connect(){
    mysql_init(&m_connection);
    mysql_options(&m_connection, MYSQL_SET_CHARSET_NAME, "utf8");
    if(!mysql_real_connect(&m_connection, m_server.c_str(), m_user.c_str(), m_password.c_str(), m_database.c_str(), 0, NULL, 0)){
        m_log.write("Error: MySQL connect failed.");
        m_log.write(mysql_error(&m_connection));
        close();
        exit(-1);
    }
}
void CLASS_MYSQL::close(){
    mysql_close(&m_connection);
}

CLASS_MYSQL_RES CLASS_MYSQL::query(std::string query){
    connect();
    CLASS_MYSQL_RES re;
    if(mysql_query(&m_connection, query.c_str())){  // != => error
        m_log.write("Query Error: " + query);
        m_log.write(mysql_error(&m_connection));
    } else {
        std::stringstream ss(query);
        std::string keyword;
        ss >> keyword;
        transform(keyword.begin(), keyword.end(), keyword.begin(), ::tolower);
        if(keyword == "select"){
            MYSQL_RES* res = mysql_store_result( &m_connection );
            m_log.write("Find: " + query);
            /* get filed_name */
            std::vector<std::string> field_name;
            MYSQL_FIELD *field;

            while(field = mysql_fetch_field(res))
                field_name.push_back(field->name);
            /* set CLASS_MYSQL_RES */
            MYSQL_ROW row;
            int num_fields = mysql_num_fields( res );
            while( row = mysql_fetch_row(res) ){
                CLASS_MYSQL_ROW tmp;
                for(int i = 0 ; i < num_fields ; i++)
                    tmp.push_back(field_name[i], row[i] != NULL ? row[i] : "NULL");
                re.push_back(tmp);
            }
            mysql_free_result( res );
        } else {
            m_log.write("Succ: " + query);
        }
    }
    close();
    return re;
}
bool CLASS_MYSQL::test(){
    connect();
    close();
    return true;
}
