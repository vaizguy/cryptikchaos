#! /usr/bin/tcsh

set PROJECT_PATH = "../../src"
set PROJECT_FILES = `du -ach $PROJECT_PATH | grep \.py$ | gawk '{print $2}'`

pep8 --statistics --benchmark $PROJECT_FILES
autopep8 $PROJECT_PATH --in-place --recursive --pep8-passes 2000 --verbose | tee -i autopep8.log
