#!/bin/bash
# Requirement:
# 	- /home/mstan/.ssh/id_rsa.pub copied to authorized_keys @maia server
# Usage:
# ./copy_report_to_maia.sh M7

[[ -z $1 ]] && MILESTONE=M0 || MILESTONE=$1
REPORT=oA_pytest_report_${MILESTONE}.html

# Rename the copy and edit the report 
cp pytest_report.html $REPORT
sed -i "s/<h1>pytest_report.html/<h1>SES 5.5 ${MILESTONE} - Openattic/" $REPORT

# Copy the report 
scp $REPORT root@10.100.96.56:/usr/share/nginx/html/
