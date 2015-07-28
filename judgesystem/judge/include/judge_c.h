#ifndef JUDGE_C_H
#define JUDGE_C_H

#include "judge.h"

#include <queue>
#include <vector>
#include <cstdio>

namespace Judge_C_namespace{
    static int compile_pid;
    void timer(int);

    class Judge_C : public Judge{
        public:
            Judge_C();
            ~Judge_C();
            virtual RESULT before_run(std::string commnad) override;
            virtual RESULT run( std::string command, 
                                std::string source=std::string(""), 
                                std::string input=std::string(""), 
                                std::string output=std::string(""),
                                std::string error=std::string("")) override ;
    };
};
#endif
