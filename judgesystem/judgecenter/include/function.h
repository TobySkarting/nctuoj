#ifndef FUNCTION_H
#define FUNCTION_H

#include <string>
#include <limits.h>
#include <unistd.h>
#include <sstream>
#include <algorithm>
#include <ctime>

std::string exec_path();
std::string judgecenter_dir();
std::string bin_dir();

int string2int(std::string);
std::string int2string(int);

struct tm get_nowtime();

#endif
