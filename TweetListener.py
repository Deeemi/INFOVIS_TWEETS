
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler, Stream
import socket,json,re
from base64 import b64encode
from hashlib import sha1

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

    twitter_stream.filter(track=['#NowPlaying'])


websocket_answer = (
    'HTTP/1.1 101 Switching Protocols',
    'Upgrade: websocket',
    'Connection: Upgrade',
    'Sec-WebSocket-Accept: {key}\r\n\r\n',
)


GUID = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"


if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # host = socket.gethostbyname(socket.gethostname())   #DAVIDE: 10.25.159.249
    host = "127.0.0.1"
    port = 9000
    s.bind((host,port))
    print ("Listening on port : %s" % str(port))
    s.listen(5)
    c,addr = s.accept()
    text = c.recv(1024)
    print("Received request from: "+str(addr))
    
    key = (re.search('Sec-WebSocket-Key:\s+(.*?)[\n\r]+', text)
    .groups()[0]
    .strip())

    response_key = b64encode(sha1(key + GUID).digest())
    response = '\r\n'.join(websocket_answer).format(key=response_key)

    c.send(response)

    sendData(c)