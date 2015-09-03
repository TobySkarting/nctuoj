#!/bin/sh
PSQL="env psql"
CONFIG="./backend/config.py"
PSQL_FILE="./psql.sql"
DBHOST=`cat $CONFIG | grep DBHOST | awk '{print $3}' | sed "s/^'//g" | sed "s/'$//g"`
DBUSER=`cat $CONFIG | grep DBUSER | awk '{print $3}' | sed "s/^'//g" | sed "s/'$//g"`
DBNAME=`cat $CONFIG | grep DBNAME | awk '{print $3}' | sed "s/^'//g" | sed "s/'$//g"`
DBPASSWORD=`cat $CONFIG | grep DBPASSWORD | awk '{print $3}' | sed "s/^'//g" | sed "s/'$//g"`
export PGPASSWORD=${DBPASSWORD}
${PSQL} -h ${DBHOST} -d ${DBNAME} -U ${DBUSER} < ${PSQL_FILE}
unset PGPASSWORD
