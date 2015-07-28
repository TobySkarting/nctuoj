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
#include "client.h"


int CLIENT::INIT(){
    m_log = LOG(log_dir() + std::string("client.log"));

    m_sock = socket(AF_INET, SOCK_STREAM, 0);
    if(m_sock == -1){
        m_log.write("Init: Error.");
        return SOCKET_INIT_ERROR;
    }

    m_server.sin_addr.s_addr = inet_addr(m_config.ip().c_str());
    m_server.sin_family = AF_INET;
    m_server.sin_port = htons(m_config.port());
    m_log.write("Init: Succ.");
    return SOCKET_INIT_SUCC;
}
int CLIENT::CONNECT(){
    if( connect(m_sock, (sockaddr*)&m_server, sizeof(m_server)) < 0){
        m_log.write("Connect: Error.");
        return SOCKET_CONNECT_ERROR;
    }
    write(m_sock, "/client_type 1\r\n", strlen("/client_type 1\r\n"));
    m_log.write("Connect Succ.");
    return SOCKET_CONNECT_SUCC;
}
CLIENT::~CLIENT(){
    CLOSE();
}
void CLIENT::CLOSE(){
    close(m_sock);
}
int CLIENT::GETSUBMISSION(){
    struct timeval timeout = {0, 0};
    while(true){
        SET_FD();
        int result = select(m_sock+1, &readfd, 0, 0, &timeout);
        if(result == 0){
            usleep(1000);
        }
        {
            int result = COMMAND_LINE();
            if(result)
                return CLIENT_CLOSE;
        }
        {
            int result = SOCK();
            if(result)
                return result;
        }
    }
}

void CLIENT::SET_FD(){
    FD_ZERO(&readfd);
    FD_SET(0, &readfd);
    FD_SET(m_sock, &readfd);
}

int CLIENT::COMMAND_LINE(){
    if(FD_ISSET(0, &readfd)){
        char buffer[BUFFER_SIZE+1];
        int result = read(0, buffer, BUFFER_SIZE);
        buffer[result-1] = 0;
        std::stringstream bufferstream(buffer);
        std::string str;
        while(getline(bufferstream, str)){
            std::stringstream ss(str);
            std::string command;
            ss >> command;
            if(command == std::string("exit")){
                return CLIENT_CLOSE;
            } else {
                write(m_sock, buffer, strlen(buffer));
            }
        }
    }
    return 0;
}
int CLIENT::SOCK(){
    if(FD_ISSET(m_sock, &readfd)){
        char buffer[BUFFER_SIZE+1];
        int result = read(m_sock, buffer, BUFFER_SIZE);
        buffer[result] = 0;
        if(result == 0){
            std::cout << "Server closed." << std::endl;
            return SERVER_CLOSE;
        } else {
            std::cout << buffer;
            std::stringstream bufferstream(buffer);
            std::string str;
            while(getline(bufferstream, str)){
                if(str.back() == '\r') str.pop_back();
                m_log.write(std::string("[From Server]: ") + str);
                std::stringstream ss(str);
                std::string command;
                ss >> command;
                if( command == std::string("/submission_id") ){
                    int submission_id;
                    ss >> submission_id;
                    return submission_id;
                } else if( command == std::string("/version") ){
                    std::string write_buffer = std::string("/version ") + VERSION + std::string("\r\n");
                    write(m_sock, write_buffer.c_str(), write_buffer.size());
                } else if( command == std::string("/update") ){
                } else if( command == std::string("/live") ){
                    write(m_sock, "/LIVE\r\n", strlen("/LIVE\r\n"));
                } else if( command == std::string("/server_close") ){
                    return SERVER_CLOSE;
                }
            }
        }
    }
    return 0;
}

void CLIENT::JUDGE_DONE(){
    write(m_sock, "/submission_done", strlen("/submission_done"));
}
