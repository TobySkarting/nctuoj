CC = g++ 
FLAGS = -std=c++11 -g -O2 
INCLUDE_DIR = ./include
SRC_DIR = ./src
BIN_DIR = ./bin
TEST_DIR = ./test
TMP_DIR = ./tmp

MYSQL = -I/usr/include/mysql -lmysqlclient

OBJS := function config log client class_mysql judge ftp

$(OBJS): %: $(TEST_DIR)/%.test.cpp  $(foreach x,$(OBJS),$(TMP_DIR)/$x.o)
	$(CC) -o $(BIN_DIR)/$(*F) $< $(foreach x, $(OBJS), $(TMP_DIR)/$x.o) -I$(INCLUDE_DIR) $(FLAGS) $(MYSQL)
	valgrind --leak-check=full --show-leak-kinds=all $(BIN_DIR)/$(*F)
	
$(foreach x,$(OBJS),$(TMP_DIR)/$x.o): $(TMP_DIR)/%.o: $(SRC_DIR)/%.cpp
	$(CC) -c $< -o $@ \
	-I$(INCLUDE_DIR) \
	$(FLAGS) \
	$(MYSQL)

clean:
	rm $(TMP_DIR)/*.o
