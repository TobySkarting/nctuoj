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
#include "judge.h"

Judge::Judge(){
    std::cout << config.mysql_server() << std::endl;
    mysql = CLASS_MYSQL(
                config.mysql_server(),
                config.mysql_user(),
                config.mysql_password(),
                config.mysql_database(),
                log_dir() + "mysql.log"
            );
    ftp = FTP(
                config.ftp_server(),
                config.ftp_user(),
                config.ftp_password(),
                log_dir() + "ftp.log"
            );
    m_log = LOG(log_dir() + "judge.log");
}

Judge::~Judge(){
}

void Judge::judge(int _submission_id){
    submission_id = _submission_id;
    m_log.write("[Submission_id: "+int2string(submission_id) + "] start judge");
    try {
        get_information();
    } catch(const char* e) {
        m_log.write("[Submission_id: "+int2string(submission_id) + "] "+e);
        std::cout << e << std::endl;
    }
    print_var(lang);
}

void Judge::get_information(){
    auto result = mysql.query("select run_type.`id`, run_type.`lang`, run_type.`only_pri`, b.problem_id FROM run_type inner join (select run_problem.`run_type_id`, run_problem.`problem_id` from run_problem inner join (select submission.`problem_id`, submission.`run_type_id` from submission where id = "+int2string(submission_id)+" limit 1) as a on run_problem.`problem_id` = a.`problem_id` and run_problem.`run_type_id` = a.`run_type_id` limit 1) as b on run_type.`id` = b.`run_type_id`;");
    if(result.empty()){
        throw "Get Information Error";
    }
    lang = string2int(result[0]["lang"]);
    run_only_pri = string2int(result[0]["only_pri"]);
    problem_id = string2int(result[0]["problem_id"]);
    run_type_id = string2int(result[0]["id"]);
}
