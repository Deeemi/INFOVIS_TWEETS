
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler, Stream
import socket,json

access_token = ""
access_secret = ""
consumer_key = ""
consumer_secret = ""

# Classe che ascolta i Tweet
class TweetsListener (StreamListener):

    def __init__(self,csocket):
        self.client_socket = csocket

    def on_data(self, data):
        try:
            msg = json.loads(data)
            print(msg['text'].encode('utf-8'))
            self.client_socket.send(msg['text'].encode('utf-8'))
            return True
        except BaseException as e:
            print ("Error on_data: %s" % str(e))
        return True

    def on_error(self, status):
        print(status)
        return True

def sendData(c_socket):
    auth = OAuthHandler(consumer_key,consumer_secret)
    auth.set_access_token(access_token,access_secret)
    twitter_stream = Stream(auth,TweetsListener(c_socket))

    #controllare coem fare filter sulla lingua
    twitter_stream.filter(languages=['en'], track=['#trump'])

if __name__ == "__main__":
    s = socket.socket()
    host = socket.gethostbyname(socket.gethostname())
    port = 5555
    s.bind((host,port))
    print ("Listening on port : %s" % str(port))
    s.listen(5)
    c,addr = s.accept()
    print("Received request from: "+str(addr))
    sendData(c)



