this is an benchmark for tcp forward server application
python + twisted
pypy   + twisted
python + gevent
go lang

benchmark result:
	           produceSocket consumerSocket     network peak       program cpu used 
python + twisted:        250             250               16M              75%
pypy   + twisted:        320             320               20M              50%
python + gevent :        150             150               10M              72%
go lang         :        200             200               12M              49%

