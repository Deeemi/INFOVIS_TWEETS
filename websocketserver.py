import json
from collections import defaultdict
from tornado import httpserver,websocket,ioloop,web
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler,Stream

# ---------------------------------------------------------------------------
# Handler per il websocket server [open, on_message, on_close, check_origin]
class WSHandler(websocket.WebSocketHandler):

    def open(self):
        print 'In ascolto di tweet'
      
    def on_message(self,message):
        access_token = "2831526055-rjEd9kv64QbenXerEvDZGpo3L5wSb9dE0ZHwwop"
        access_token_secret = "QO3MoIovhutEbgGGZsMcssH2l7moqS4YjSlcqx5DlsQyF"
        consumer_key = "ZuM1tKSWM2ifzOBtF5YZ1foWD"
        consumer_secret = "vylwHFzWtSBgnULX8PTkb7y46SX1mvl81EBc6eCXfONHM96ZWd"

        hashtags = message.split(' ')
        counts = {}
        for hashtag in hashtags:
        	counts[hashtag[1:].lower()] = {'Tweets_Counter': 0}
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        stream = Stream(auth, TweetsListener(self,counts))
        stream.filter(track=hashtags,async=True)
 
    def on_close(self):
        print 'Connessione chiusa'
 
    def check_origin(self,origin):
        return True
        
# URI dell'handler
application = web.Application([
    (r'/ws', WSHandler),
])

# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# Ascoltatore di tweets [on_data, on_error, ws e' il WSHandler]
class TweetsListener(StreamListener):

    def __init__(self,ws,counts):
        self.ws = ws
        self.counts = counts

    def on_data(self,data):
        try:
            
            msg = json.loads(data)
            hashtags = msg['entities']['hashtags']
            mainhashtag = ''

            for hashtag in hashtags:
                if hashtag['text'].lower() in self.counts.keys():
                    mainhashtag = hashtag['text'].lower()
                    break
            
            if mainhashtag != '':
                self.counts[mainhashtag]['Tweets_Counter'] += 1
                for hashtag in hashtags:
                    if hashtag['text'].lower() != mainhashtag:
                        if hashtag['text'].lower() in self.counts[mainhashtag]:
                            self.counts[mainhashtag][hashtag['text'].lower()] = (self.counts[mainhashtag][hashtag['text'].lower()][0]+1,self.counts[mainhashtag][hashtag['text'].lower()][1])
                        else:
                            self.counts[mainhashtag][hashtag['text'].lower()] = (1,defaultdict(int))
                        for x in hashtags:
                            if x['text'].lower()!=hashtag['text'].lower() and x['text'].lower()!=mainhashtag:
                                self.counts[mainhashtag][hashtag['text'].lower()][1][x['text'].lower()] += 1
            
            self.ws.write_message(self.counts)           
            return True
        
        except BaseException as e:
            return False

    def on_error(self,status):
        print(status)
        return True

# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# messa in ascolto del websocket server
if __name__ == "__main__":
    http_server = httpserver.HTTPServer(application)
    port = 9000
    http_server.listen(port)
    myIP = '127.0.0.1'
    print('*** Websocket Server in ascolto su '+myIP+':'+str(port)+'***')
    ioloop.IOLoop.instance().start()

# ---------------------------------------------------------------------------