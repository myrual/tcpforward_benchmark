this is an benchmark for tcp forward server application
====================================

* python + twisted
* pypy   + twisted
* python + gevent
* go lang

| solution | max forward socket | peak stable network data |
| ------------ | ------------- | ------------ |
| python26+twisted | 250  | 16M |
| pypy27+twisted | 320  | 20M |
| python26+gevent | 400  | 22M |
| go lang | 400  | 24M |
