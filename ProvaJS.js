var net = require('net');
var client = new net.Socket();
var HOST='127.0.0.1';
var PORT='9000';

var MSG="{\"REQUEST\":\"STATUS\"}";    
var socketmessage;

getSocketMessage(MSG);

function getSocketMessage(tcpmsg){
  var outData;

  client.connect(PORT, HOST, function() {
    console.log("Client: " + tcpmsg);
    client.write(tcpmsg);
  });

  //client.setTimeout(9000, function() {  client.destroy(); });

  client.on('data', function(data) {
    console.log('Server: ' + data.toString('utf8').replace(/[#][A-Za-z]+|http[A-Za-z0-9:/.]+/g, "").replace(/[^a-zA-Z0-9 -]/g, ""));
    //client.destroy();
  });

  //Add a 'close' event handler for the client socket
  client.on('close', function() {
    console.log('Connection closed');
  });

  // Add a 'error' event handler for the client socket
  client.on('error', function(error) {
    console.log('Error Connection: ' + error);
  });
}