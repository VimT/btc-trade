#!/home/btc/python3/bin/python
# encoding=utf-8
# 返回账户余额信息的cgi文件
# 将余额与冻结余额加在一起返回
import sys
sys.path.append("..")
from  trade import *
import json
import cgi
import cgitb
import time
INIT_MONEY = 100
def main():
	cgitb.enable()
	period_arr = [PERIOD_M1,PERIOD_M5,PERIOD_M15,PERIOD_M30,PERIOD_H1,PERIOD_D1]
	asset = exchange.GetAccount()#返回的账户信息
	lastPrice = exchange.GetTicker().Last#返回市场信息
	# profit = asset.Balance+asset.FrozenBalance + lastPrice * (asset.Stocks+asset.FrozenStocks) - INIT_MONEY
	profit = asset.NetAsset - INIT_MONEY
	data = {'Balance': asset.Balance+asset.FrozenBalance, 
			'Stocks': asset.Stocks+asset.FrozenStocks,
			'Profit': round(profit,2), 'NetAsset': asset.NetAsset} #Balance表示余额 Stock表示比特币数目
	data = json.dumps(data)
	info =  "status:200 ok\nContent-type:application/json\nLength:%d\n\n%s" % (len(data),data)
	print (info)
	#for record in recs:
	#	print (record)
if __name__ == "__main__":
	main()
