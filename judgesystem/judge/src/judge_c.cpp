#include "judge_c.h"

Judge_C_namespace::Judge_C::Judge_C(){
}
Judge_C_namespace::Judge_C::~Judge_C(){
}
void Judge_C_namespace::timer(int sig){
    kill(Judge_C_namespace::compile_pid, SIGUSR1);
}
RESULT Judge_C_namespace::Judge_C::before_run(std::string command){
    RESULT re;
    EXECL_PAR execl_par;
    Judge_C_namespace::compile_pid = fork();
    bool alarm_scheduled = false;
    auto calc_usage_time_ms = [](rusage rinfo){
        return (rinfo.ru_utime.tv_sec+rinfo.ru_stime.tv_sec)*1000
                +( rinfo.ru_utime.tv_usec+rinfo.ru_stime.tv_usec)/1000;
    };

    signal(SIGALRM, Judge_C_namespace::timer);
     

    if(Judge_C_namespace::compile_pid){
        rusage rinfo;
        int status;
        bool done = false;
        while(1){
            wait4(Judge_C_namespace::compile_pid, &status, 0, &rinfo);
            if(!alarm_scheduled){
                ualarm(1000, 1000);
                alarm_scheduled = true;
            }
            if(WIFEXITED(status)){
                done = true;
                break;
            }
                std::cout << calc_usage_time_ms(rinfo) << std::endl;
            if(calc_usage_time_ms(rinfo) > 100){
                break;
            }
            ptrace(PTRACE_SYSCALL, Judge_C_namespace::compile_pid, NULL, NULL);
        }
        alarm(0);
        /* compile error */
        std::cout << done << std::endl;
        if(!done){
            std::vector<int> process[65536];
            FILE *pfile = popen("ps -e -o ppid= -o pid=", "r");
            int ppid, pid;
            while(fscanf(pfile, "%d %d", &ppid, &pid)!=EOF)
                process[ppid].push_back(pid);
            fclose(pfile);
            std::queue<int> kill_queue;
            kill_queue.push(compile_pid);
            while(kill_queue.size()){
                int process_id = kill_queue.front();
                kill_queue.pop();
                kill(process_id, SIGKILL);
                waitpid(process_id, 0, 0);
                for(int i = 0 ; i < (int)process[process_id].size() ; i++)
                    kill_queue.push(process[process_id][i]);
            }
        }
    } else {
        ptrace(PTRACE_TRACEME, Judge_C_namespace::compile_pid, NULL, NULL);
        execv(lang_path[LANG_C],  execl_par.parse(command));
    }
    return re;
}

RESULT Judge_C_namespace::Judge_C::run(std::string command, std::string source, std::string input, std::string ouput, std::string error){
    RESULT re;
    return re;
}
