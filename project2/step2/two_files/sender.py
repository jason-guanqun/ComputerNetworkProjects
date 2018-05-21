#!/usr/bin/python
import socket
import argparse
import random
import time
import datetime
import os
import json
import thread
import threading

# Command line parameters
parser = argparse.ArgumentParser(description='UDP sender')
parser.add_argument('-l', dest='loss_rate', action='store', default=0, type=float)
parser.add_argument('-p', dest='rec_port_num', action='store', default=5001, type=int)
args, unknownargs = parser.parse_known_args()

# get arguments
loss_rate = args.loss_rate
rec_port_num = args.rec_port_num

# extract IPs and Ports
UDP_IPs = [each.split(':')[0] for each in unknownargs]
UDP_PORTs = [each.split(':')[1] for each in unknownargs]

# message sent
MESSAGE = "Hello, World!"

# delete the log file if it exists
if os.path.exists("loggings.txt"):
	os.remove("loggings.txt")
	# window.append(send_dict)
	# print window
	# if all_packets:
	# 	data = all_packets[0]
	# 	del(all_packets[0])
	# else:
	# 	finish = True
	

########################     Step 1   ##############################
# index = 0
# while True:
# 	if index > len(UDP_IPs)-1:
# 		index = 0
# 	# generate random number
# 	gen_rand_num = random.random()
# 	if gen_rand_num < loss_rate:
# 		print "Packet Lost!"
# 		time.sleep(1)
# 		continue
	
# 	UDP_IP = UDP_IPs[index]
# 	UDP_PORT = int(UDP_PORTs[index])
# 	# UDP_IP = UDP_IPs[0]
# 	# UDP_PORT = int(UDP_PORTs[0])

# 	sock = socket.socket(socket.AF_INET, # Internet
# 	             socket.SOCK_DGRAM) # UDP
# 	sock.bind(('', rec_port_num))
# 	sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
# 	try:
# 		message, address = sock.recvfrom(1024)
# 		print message
# 	except socket.timeout:
# 		print('REQUEST TIMED OUT')
# 	log_time = " ".join(message.split(" ")[:2])
# 	print log_time + " localhost " + address[0] + ":" + str(address[1])

# 	index +=1 
# 	time.sleep(1)

# print "Transmission complete!"
########################     Step 1   ##############################



# thread.start_new_thread(self.handle_requests, (browser_socket, conn, addr))



########################     A test send    ##############################
# UDP_IP = UDP_IPs[0]
# UDP_PORT = int(UDP_PORTs[0])
sock = socket.socket(socket.AF_INET, # Internet
	             socket.SOCK_DGRAM) # UDP
sock.bind(('', rec_port_num))
# send_dict = {"SEQ" : 1, "ACK" : 0}
# send_message = json.dumps(send_dict)
# sock.sendto(send_message, (UDP_IP, UDP_PORT))

# while True:
# 	received_data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
# 	received_json = json.loads(received_data)
# 	print received_json["SEQ"], addr

# 	exit()


########################     Only one destination    ##############################
# TIME_OUT = 0.5
# window_size = 5
# base = 1
# nextseqnum = 1
# last_time = time.time()
# sock.settimeout(0.001)

# while True:
# 	if (nextseqnum<base+window_size):
# 		if random.random() < loss_rate:
# 			print "Packet ", nextseqnum, " Loss!"
# 			nextseqnum += 1
# 		else:
# 			rdt_send()
# 	try:
# 		received_data, server_addr = sock.recvfrom(1024)
# 		received_ack_num = json.loads(received_data)["ACK"]
# 		print "Received ACK for: ", received_ack_num
# 		if received_ack_num == -1:
# 				break
# 		base = received_ack_num + 1
# 		last_time = time.time()
# 	except:
# 		now_time = time.time()
# 		if (now_time - last_time > TIME_OUT):
# 			for i in range(base, nextseqnum):
# 				send_packet=make_pkt(i)
# 				sock.sendto(send_packet, (UDP_IP, UDP_PORT))
# 				print "Time Out! ", "Resend data: ", i

# print "Transmission Complete!"
# sock.close()

########################     Multiple destinations    ##############################
def for_each_dest(UDP_IP, UDP_PORT):
	window_size = 5
	TIME_OUT = 0.5
	last_time = time.time()
	sock.settimeout(0.001)

	class local:
		base = 1
		nextseqnum = 1
		
	def make_pkt(num):
		send_dict = {"SEQ" : num, "ACK" : 0, "Data": "test"}
		send_packet=json.dumps(send_dict)
		return send_packet

	def rdt_send():
		send_packet=make_pkt(local.nextseqnum)
		sock.sendto(send_packet, (UDP_IP, UDP_PORT))
		print "Send data", local.nextseqnum
		local.nextseqnum += 1

	while True:
		if (local.nextseqnum < local.base+window_size):
			if random.random() < loss_rate:
				print "Packet ",local.nextseqnum, " Loss!"
				local.nextseqnum += 1
			else:
				rdt_send()
		try:
			received_data, server_addr = sock.recvfrom(1024)
			received_ack_num = json.loads(received_data)["ACK"]
			print "Received ACK for: ", received_ack_num
			if received_ack_num == -1:
					break
			local.base = received_ack_num + 1
			if local.base == local.nextseqnum:
				last_time = time.time()
		except:
			now_time = time.time()
			if (now_time - last_time > TIME_OUT):
				for i in range(local.base, local.nextseqnum):
					send_packet=make_pkt(i)
					sock.sendto(send_packet, (UDP_IP, UDP_PORT))
					print "Time Out! ", "Resend data: ", i

	print "Transmission Complete!"
	sock.close()


for UDP_IP, UDP_PORT in zip(UDP_IPs, UDP_PORTs):
	# thread.start_new_thread(for_each_dest, (UDP_IP, UDP_PORT))
	t = threading.Thread(target = for_each_dest, args = (UDP_IP, int(UDP_PORT)))
	t.start()