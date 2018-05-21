#!/usr/bin/python
import socket
import json
import argparse

UDP_IP = "127.0.0.1"
# UDP_PORT = 5005
parser = argparse.ArgumentParser(description='UDP receiver')
parser.add_argument('-p', dest='rec_port_num', action='store', default=5001, type=int)
args, unknownargs = parser.parse_known_args()

UDP_PORT = args.rec_port_num

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

expectedseqnum = 1
ACK = 1
count = 0 
finish = False

def rdt_rcv(received_data, address):
    global expectedseqnum, finish, count
    received_json = json.loads(received_data)
    received_ack_num = received_json["SEQ"]
    # if seccessfully receive expected sequence number
    if received_ack_num == expectedseqnum:
      print "Received inorder package: ", received_ack_num, "Expected: ", expectedseqnum
      count +=1
      # If I successfully receive 100 packages 
      if count == 100:
        finish = True
        send_dict = {"SEQ" : -1, "ACK" : -1}
        send_packet = json.dumps(send_dict)
        sock.sendto(send_packet, (address[0], address[1]))
        return
      expectedseqnum += 1
      send_dict = {"SEQ" : -1, "ACK" : received_ack_num}
      send_packet = json.dumps(send_dict)
      sock.sendto(send_packet, (address[0], address[1]))
    # Resend previous ACK
    else:
      print "Received out of order", received_ack_num, "Expected: ", expectedseqnum
      send_dict = {"SEQ" : -1, "ACK" : expectedseqnum-1}
      send_packet = json.dumps(send_dict)
      sock.sendto(send_packet, (address[0], address[1]))

while not finish:
  data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
  rdt_rcv(data, addr)

print "Collection done!"
sock.close()