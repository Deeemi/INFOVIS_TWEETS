import json
from collections import defaultdict
from tornado import httpserver,websocket,ioloop,web
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler, Stream

# ---------------------------------------------------------------------------
# Handler per il websocket server [open, on_message, on_close, check_origin]
class WSHandler(websocket.WebSocketHandler):

    def open(self):
        print ('In ascolto di tweet')
      
    def on_message(self, message):
        if message=='Start':           
            access_token = "479635577-RggBMFaIFh9HkbC5JMwNj1KsnWbaYvJusrzNEYvT"
            access_token_secret = "RD58EwiM6uxbNnq1cOxDxr06emV0HuimoGDgw40zFPYIX"
            consumer_key = "gS7DkeN3SlL6DtG4XR3e5rWnb"
            consumer_secret = "cPCT9xJhQYJh2gRaAqu5K2V7bZERkfv3t2TcZpadswO9sRzoxN"

            auth = OAuthHandler(consumer_key, consumer_secret)
            auth.set_access_token(access_token, access_token_secret)
            stream = Stream(auth, TweetsListener(self)) 
            stream.filter(track=['#gameofthrones','#amazon','#ferrari'],async=True)
 
    def on_close(self):
        print ('Connessione chiusa')
 
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

    def __init__(self,ws):
        self.ws = ws
        self.counts = { 'gameofthrones':defaultdict(int),'amazon':defaultdict(int),'ferrari':defaultdict(int)
                      }

    def on_data(self, data):
        try:
            msg = json.loads(data)
            hashtags = msg['entities']['hashtags']
            print(hashtags)
            mainhashtag = ''
            for hashtag in hashtags:
                if hashtag['text'].lower() in ['gameofthrones','amazon','ferrari']:
                    mainhashtag = hashtag['text'].lower()
                    break
            for hashtag in hashtags:
                if hashtag['text'].lower() != mainhashtag:
                    self.counts[mainhashtag][hashtag['text'].lower()] += 1
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