#!/home/btc/python3/bin/python
# encoding=utf-8
from trade import *
from trade import dao
import json
import cgi
import cgitb
import time
def main():
	cgitb.enable()
	period_arr = [PERIOD_M1,PERIOD_M5,PERIOD_M15,PERIOD_M30,PERIOD_H1,PERIOD_D1]
	form = cgi.FieldStorage()
#	period_str1 = form.getvalue('period')
	MAX_TRANS_ITEM = 100 #最大的返回条目数量
	result = dao.select_trade(MAX_TRANS_ITEM)
	data = {'trans': []}
	for row in result:
		item = {'id':row[0], 'price':row[1], 'time':row[2].strftime("%Y-%m-%d %H:%M:%S"), 
		'order_amount': row[3], 'type':row[4], 'final_amount':row[5], 'fee':row[6]}
		item['fee'] = round(item['final_amount']*0.002, 2)
		#if item['type'] == '市价买':
		#	item['fee'] = round(item['final_amount']*0.002, 2)
		#else:
		#	item['fee'] = round(item['price']*item['final_amount']*0.002, 2)
		# id = row[0] #交易id
		# price = row[1] #平均成交价格
		# time = row[2]  #时间
		# order_amount = row[3] #委托交易数量
		# Type = row[4] #交易类型
		# final_amount = row[5] #交易额
		# fee = row[6] #手续费
		data['trans'].append(item)

	#print (result)
	data = json.dumps(data)
	#data = {"retcode":0,"data":"hello"}
	#data = json.dumps(data)
	info =  "status:200 ok\nContent-type:application/json\nLength:%d\n\n%s" % (len(data),data)
	print (info)
	#for record in recs:
	#	print (record)
if __name__ == "__main__":
	main()
