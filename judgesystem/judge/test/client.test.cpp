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
#include <iostream>
#include <unistd.h>
#include "client.h"
#include "judge.h"

using namespace std;
int main(){
    Judge judge;
    /*
    judge.judge(1);
    return 0;
    */
    int err_delay_time = 0;
    int err_delay_array[] = {1, 5, 10, 30, 60};
    while(1){
        CLIENT client;
        if(client.INIT() != SOCKET_INIT_SUCC){
            usleep(err_delay_array[err_delay_time] * 1e6);
            err_delay_time = min(err_delay_time + 1, 4);
            cout << err_delay_array[err_delay_time] << endl;;
            continue;
        }
        err_delay_time = 0;
        while(client.CONNECT() != SOCKET_CONNECT_SUCC){
            cout << err_delay_array[err_delay_time] << endl;;
            usleep(err_delay_array[err_delay_time] * 1e6);
            err_delay_time = min(err_delay_time + 1, 4);
            continue;
        }
        err_delay_time = 0;

        int result = 0;
        while(1){
            result = client.GETSUBMISSION();
            if(result == SERVER_CLOSE)
                break;
            if(result == CLIENT_CLOSE)
                return 0;
            judge.judge(result);
            client.JUDGE_DONE();
        }
    }
    return 0;
}
