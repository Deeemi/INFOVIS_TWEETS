import json
from tornado import httpserver,websocket,ioloop,web
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler, Stream

# ---------------------------------------------------------------------------
# Handler per il websocket server [open, on_message, on_close, check_origin]
class WSHandler(websocket.WebSocketHandler):

    def open(self):
        print 'new connection'
      
    def on_message(self, message):
        if message=='Start':
            access_token = ""
            access_token_secret = ""
            consumer_key = ""
            consumer_secret = ""

            auth = OAuthHandler(consumer_key, consumer_secret)
            auth.set_access_token(access_token, access_token_secret)
            stream = Stream(auth, TweetsListener(self)) 
            stream.filter(track=['#NowPlaying'],async=True)
 
    def on_close(self):
        print 'connection closed'
 
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

    def on_data(self, data):
        try:
            msg = json.loads(data)
            print(msg['text'].encode('utf-8'))
            self.ws.write_message(msg['text'].encode('utf-8'))
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
