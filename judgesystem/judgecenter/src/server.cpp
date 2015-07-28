#include "server.h"


#define DEBUG_MODE


SERVER::SERVER(){
}
SERVER::~SERVER(){
    stop();
}
void SERVER::Set_FD(){
    FD_ZERO(&readfd);
    FD_SET(0, &readfd); //stdin
    FD_SET(m_server_socket, &readfd);
    for(auto it : m_client_list)
        FD_SET(it.socket, &readfd);
}
void SERVER::Server(){
    if(FD_ISSET(m_server_socket, &readfd)){
        CLIENT new_client;
        new_client.socket = accept(m_server_socket, (sockaddr*)&m_server, (socklen_t*)&m_server_len);
        new_client.busy = false;
        new_client.addr_len = sizeof(new_client.addr);
        getpeername(new_client.socket, (sockaddr*)&new_client.addr, &new_client.addr_len);
        char t_ip[32];
        inet_ntop(AF_INET, &new_client.addr.sin_addr, t_ip, sizeof(t_ip));
        new_client.ip = std::string(t_ip);
        m_client_list.push_back(new_client);
        std::cout << "New Connection: " << new_client.ip << std::endl;
    }
}
void SERVER::Client(){
    int result;
    char buffer[BUFFER_SIZE+1];
    for(std::list<CLIENT>::iterator it = m_client_list.begin() ; it != m_client_list.end() ;){
        if(FD_ISSET(it->socket, &readfd)){
            int result = read(it->socket, buffer, BUFFER_SIZE);
            buffer[result] = 0;
            if( result == 0){
                std::cout << "Close Connection: [" << it->ip << "/" << it->client_type << "]" << std::endl;
                std::list<CLIENT>::iterator tmp = it;
                it = ++it;
                m_client_list.erase(tmp);
                continue;
            } else {
                int re = MSG_ERR;
                it->last_active = get_nowtime();
                std::string str_buffer(buffer);
                if(it->client_type == CLIENT_TYPE_WAIT){
                    re = Client_Wait(it, str_buffer);
                } else if(it->client_type == CLIENT_TYPE_JUDGE){
                    re = Client_Judge(it, str_buffer);
                } else if(it->client_type == CLIENT_TYPE_WEB){
                    re = Client_Web(it, str_buffer);
                }
                if(re == MSG_ERR){
                    close(it->socket);
                    std::list<CLIENT>::iterator tmp = it;
                    it = ++it;
                    m_client_list.erase(tmp);
                    continue;
                }
            }
        }
        ++it;
    }
}
int SERVER::Client_Wait(std::list<CLIENT>::iterator it, std::string buffer){
    std::stringstream bufferstream(buffer);
    std::string str;
    while(getline(bufferstream, str)){
        std::cout << "Form [" << it->ip << "/" << it->client_type << "]: " <<  str;
        std::stringstream ss(str);
        std::string command;
        ss >> command;

        if(command == std::string("/client_type")){
            ss >> (it->client_type);
            return MSG_SUCC;
        } else if( command == std::string("/LIVE") && it->live_notify == true){
            it->live_notify = 0;
            return MSG_SUCC;
        } else {
            return MSG_ERR;
        }
    }
}
int SERVER::Client_Judge(std::list<CLIENT>::iterator it, std::string buffer){
    std::stringstream bufferstream(buffer);
    std::string str;
    while(getline(bufferstream, str)){
        std::cout << "Form [" << it->ip << "/" << it->client_type << "]: " <<  str;
        std::stringstream ss(str);
        std::string command;
        ss >> command;

        if(command == std::string("/submission_done") && it->busy == true){
            it->busy = false;
            return MSG_SUCC;
        } else if( command == std::string("/LIVE") && it->live_notify == true){
            it->live_notify = 0;
            return MSG_SUCC;
        } else if( command == std::string("/version")){
            std::string version;
            ss >> version;
            if(version != VERSION){
                std::cout << "XD" << std::endl;
                write(it->socket, "/update\r\n", strlen("/update\r\n"));
            }
        } else {
            return MSG_ERR;
        }
    }
}
int SERVER::Client_Web(std::list<CLIENT>::iterator it, std::string buffer){
    return MSG_ERR;
}
int SERVER::Command_Line(){
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
            if(command == std::string("exit")) {
                return SERVER_EXIT;
            } else if(command == std::string("restart")) {
                stop();
                return SERVER_RESTART;
#ifdef DEBUG_MODE
            } else if(command == std::string("/version")) {
                for(auto &client : m_client_list)
                    write(client.socket, "/version\r\n", strlen("/version\r\n"));
            } else if(command == std::string("/mysql")) {
                std::string mysql_query;
                getline(ss, mysql_query);
                m_mysql.query(mysql_query);
#endif
            }

        }
    }
    return 0;
}
void SERVER::Idle_Check(){
    static struct tm last_check = get_nowtime();
    struct tm now = get_nowtime();
    //update each second
    const int timeout_notify = 300;
    const int timeout_kick   = 360;
    //const int timeout_notify = 5;
    //const int timeout_kick   = 10;
    if(difftime(mktime(&last_check), mktime(&now))){
        for(std::list<CLIENT>::iterator it = m_client_list.begin() ; it != m_client_list.end() ;){
            int diff = difftime(mktime(&now), mktime(&(it->last_active)));
            if(diff >= timeout_kick){
                close(it->socket);
                std::list<CLIENT>::iterator tmp = it;
                it = ++it;
                m_client_list.erase(tmp);
                continue;
            } else if(diff >= timeout_notify && !(it->live_notify)){
                it->live_notify = true;
                write(it->socket, "/live\r\n", strlen("/live\r\n"));
            }
            ++it;
        }
        last_check = get_nowtime();
    }
}
void SERVER::Get_Submission(){
    static struct tm last_update = get_nowtime();
    struct tm now = get_nowtime();
    //update each second
    if(difftime(mktime(&last_update), mktime(&now))){
        auto result = m_mysql.query("select * from wait_submission");
        for(auto &x : result){
            char buffer[BUFFER_SIZE+1];
            sprintf(buffer, "[GetSubmission]: wait_submission id: %s submission_id: %s", x["id"].c_str(), x["submission_id"].c_str());
            std::cout << buffer << std::endl;
            m_log.write(buffer);
            // delete from wait_submission where id=x["id"]
            m_mysql.query(std::string("delete from wait_submission where id=")+x["id"]);
            m_submission_list.push_back(string2int(x["submission_id"]));
        }
        last_update = get_nowtime();
    }
}
void SERVER::Sent_Submission(){
    for(auto &client : m_client_list){
        if((client.busy == false) && m_submission_list.size()){
            client.busy = true;
            client.submission_id = m_submission_list.front();
            m_submission_list.pop_front();
            /* sent submission */
            std::string buffer = std::string("/submission_id ") + int2string(client.submission_id) + std::string("\r\n");
            write(client.socket, buffer.c_str(), buffer.size()); 
            std::cout << client.ip << ' ' << buffer;
        }
    }
}
int SERVER::start(){
    m_log = LOG("server.log");
    m_config = CONFIG();
    std::cout << m_config.mysql_server() << std::endl;
    m_mysql = CLASS_MYSQL(m_config.mysql_server(), m_config.mysql_user(), m_config.mysql_password(), m_config.mysql_database());
    
    if(m_mysql.test()){
    } else {
        return 1001;
    }

	if( (m_server_socket = socket(AF_INET, SOCK_STREAM, 0)) == 0){
        return 1002;
	}

    int m_opt = 1;  //re use addr port
    if( setsockopt(m_server_socket, SOL_SOCKET, SO_REUSEADDR, &m_opt, sizeof(m_opt)) < 0){
        return 1003;
    }
    if(setsockopt(m_server_socket, SOL_SOCKET, SO_REUSEPORT, &m_opt,sizeof(m_opt)) < 0){
        return 1004;
    }

	int port = m_config.port();
	int max_wait_listen = m_config.max_wait_listen();
    std::cout << port << ' ' << max_wait_listen << std::endl;

	m_server.sin_family = AF_INET;
	m_server.sin_addr.s_addr = INADDR_ANY;
	m_server.sin_port = htons( port );

	if( bind(m_server_socket, (sockaddr *)&m_server, sizeof(m_server)) < 0){
        return 1005;
	}

	if( listen(m_server_socket, max_wait_listen) < 0){
		return 1006;
	}

	m_server_len = sizeof(m_server);

	struct timeval timeout={0, 0};
    

	while(true){
        Set_FD();

        int max_sd = m_server_socket;
        for(auto it : m_client_list)
            max_sd = max_sd > it.socket ? max_sd : it.socket;

        int result = select(max_sd + 1, &readfd, NULL, NULL, &timeout);

        Get_Submission();
        Idle_Check();
        Sent_Submission();
        if(result == 0){
            usleep(10000);
            continue;
        }
        {
            int com_result = Command_Line();
            if(com_result == SERVER_EXIT || com_result == SERVER_RESTART)
                return com_result;
        }
        {
            Server();
        }
        {
            Client();
        }
	}
}

void SERVER::stop(){
    for(auto &submission_id : m_submission_list)
        m_mysql.query("insert into wait_submission (`submission_id`) VALUES ('" + int2string(submission_id) + "')");
    for(auto &client : m_client_list)
        close(client.socket);
    m_submission_list.clear();
    m_client_list.clear();
    close(m_server_socket);
}
