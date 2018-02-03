#! /bin/bash
liquibase --defaultsFile=$1  --changeLogFile=$2 updateSQL

