#!/home/btc/python3/bin/python
# encoding=utf-8
from trade import *
import json
import cgi
import cgitb
import time
def main():
	cgitb.enable()
	period_arr = [PERIOD_M1,PERIOD_M5,PERIOD_M15,PERIOD_M30,PERIOD_H1,PERIOD_D1]
	form = cgi.FieldStorage()
	period_str1 = form.getvalue('period')
#	period_str2 = form.getvalue("period2")
	period_id1 = period_arr[int(period_str1)]
#	period_id2 = period_arr[int(period_str2)]
	#if not form.has_key("period"):
	#	pass
		#period = period_arr[0]
	#else:
	#	period = period_arr[int(form.getvalue("period"))]
	recs1 = exchange.GetRecords(period_id1)
#	recs2 = exchange.GetRecords(period_id2)
	record_arr = []
#	record2 = []
	for record in recs1:
		#time_str = "123"
		time_str = time.strftime('%Y-%m-%d %H:%M',time.localtime(record.Time/1000.0))
		record_arr.append([time_str,record.Open,record.Close,record.Low,record.High])
		#record1.append({"时间":time_str,"开盘价":record.Open,"最高价":record.High,"最低价":record.Low,"收盘价":record.Close,"交易量":record.Volume})
#	for record in recs2:
#		record2.append({"时间":record.Time,"开盘价":record.Open,"最高价":record.High,"最低价":record.Low,"收盘价":record.Close,"交易量":record.Volume})
#	record_arr.append(record2)
	data = {"retcode":0,"recs":record_arr}
	data = json.dumps(data)
	#data = {"retcode":0,"data":"hello"}
	#data = json.dumps(data)
	info =  "status:200 ok\nContent-type:application/json\nLength:%d\n\n%s" % (len(data),data)
	print (info)
	#for record in recs:
	#	print (record)
if __name__ == "__main__":
	main()
