#!/home/btc/python3/bin/python
# encoding=utf-8
import time
import fcntl
import os
def trade_fun(start_time,end_time):
	file_name = "run_flag"
	if not os.path.exists(file_name):
		f = open(file_name,"w")
		f.close()
		#call main function
