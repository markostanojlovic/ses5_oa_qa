#!/bin/bash

# running all test cases as suite
# example: 
# 		python name_of_test_cases_file.py 
# example one TC only: 
#		python name_of_test_cases_file.py class_name.TC_name

echo " Executing test cases:"
echo 
echo 

function echo_limiter {
echo 
echo "-----------------------------------------------------"
echo 
}

python pool_new.py
echo_limiter
python pool_edit.py
echo_limiter
python pool_delete.py
echo_limiter
python rbd_img_new.py
echo_limiter




