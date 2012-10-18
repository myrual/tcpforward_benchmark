this is an benchmark for tcp forward server application
python + twisted
pypy   + twisted
python + gevent
go lang

benchmark result:   

	           produceSocket consumerSocket     network peak       program cpu used     

python + twisted:        250             250               16M              75%    

pypy   + twisted:        320             320               20M              50%    

python + gevent :        260             260               13M              60%    

go lang         :        400             400               24M              49%   


