#include <bits/stdc++.h>
using namespace std;

string judgecenter_server;
string judgecenter_port;
string judgecenter_max_wait_listen;

string mysql_server;
string mysql_user;
string mysql_password;
string mysql_database;

string ftp_server;
string ftp_directory;
string ftp_user;
string ftp_password;
bool Get();
void WriteToJudgeCenter();
void WriteToJudge();
int main(){
	
	while(!Get());
	WriteToJudgeCenter();
	WriteToJudge();
	return 0;
}
bool Get(){
	cout << "judgecenter server: ";
	cin >> judgecenter_server;
	cout << "judgecenter port: ";
	cin >> judgecenter_port;
	cout << "judgecenter max wait listen(Please enter 4 if you don't know what it is): ";
	cin >> judgecenter_max_wait_listen;

	cout << endl;

	cout << "mysql server: ";
	cin >> mysql_server;
	cout << "mysql user: ";
	cin >> mysql_user;
	cout << "mysql password: ";
	cin >> mysql_password;
	cout << "mysql database: ";
	cin >> mysql_database;

	cout << endl;

	cout << "ftp server: ";
	cin >> ftp_server;
	cout << "ftp directory( / means your home): ";
	cin >> ftp_directory;
	cout << "ftp user: ";
	cin >> ftp_user;
	cout << "ftp password: ";
	cin >> ftp_password;
	

	string flag;
	cout << "All thing correct?(YES/NO): ";
	cin >> flag;
	if( flag == "YES" ) return true;
	return false;
}
void WirteToJudgeCenter(){
	ifstream ifs;
	ifs << judgecenter_server << endl;
	ifs << judgecenter_port << endl;
	ifs << judgecenter_max_wait_listen << endl;
	
	ifs << mysql_server << endl;
	ifs << mysql_user << endl;
	ifs << mysql_password << endl;
	ifs << mysql_database << endl;
	ifs.close();
}
void WriteToJudge(){
	ifstream ifs;
	ifs << judgecenter_server << endl;
	ifs
}
