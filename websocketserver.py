import json
from tornado import httpserver,websocket,ioloop,web
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler, Stream

# ---------------------------------------------------------------------------
# Handler per il websocket server [open, on_message, on_close, check_origin]
class WSHandler(websocket.WebSocketHandler):

    def open(self):
        print 'In ascolto di tweet'
      
    def on_message(self, message):
        access_token = "479635577-RggBMFaIFh9HkbC5JMwNj1KsnWbaYvJusrzNEYvT"
        access_token_secret = "RD58EwiM6uxbNnq1cOxDxr06emV0HuimoGDgw40zFPYIX"
        consumer_key = "gS7DkeN3SlL6DtG4XR3e5rWnb"
        consumer_secret = "cPCT9xJhQYJh2gRaAqu5K2V7bZERkfv3t2TcZpadswO9sRzoxN"

        hashtags = message.split(' ')
        counts = {}
        for hashtag in hashtags:
        	counts[hashtag] = {}
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        stream = Stream(auth, TweetsListener(self,counts)) 
        stream.filter(track=['#'+x for x in hashtags],async=True)
 
    def on_close(self):
        print 'Connessione chiusa'
 
    def check_origin(self, origin):
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

    def on_data(self, data):
        try:
            msg = json.loads(data)
            hashtags = msg['entities']['hashtags']
            mainhashtag = ''
            for hashtag in hashtags:
                if hashtag['text'].lower() in self.counts.keys():
                    mainhashtag = hashtag['text'].lower()
                    break
            if mainhashtag != '':
                for hashtag in hashtags:
                    if hashtag['text'].lower() != mainhashtag:
                        if hashtag['text'].lower() in self.counts[mainhashtag]:
                            tmp_count = self.counts[mainhashtag][hashtag['text'].lower()][0]
                            tmp_list = self.counts[mainhashtag][hashtag['text'].lower()][1]
                            self.counts[mainhashtag][hashtag['text'].lower()] = (tmp_count+1,list(set(tmp_list+[x['text'].lower() for x in hashtags if x['text'].lower()!=hashtag['text'].lower() and x['text'].lower()!=mainhashtag])))
                        else:
                            self.counts[mainhashtag][hashtag['text'].lower()] = (1,list(set([x['text'].lower() for x in hashtags if x['text'].lower()!=hashtag['text'].lower() and x['text'].lower()!=mainhashtag])))
            self.ws.write_message(self.counts)
            return True
        except BaseException as e:
            return False

    def on_error(self, status):
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