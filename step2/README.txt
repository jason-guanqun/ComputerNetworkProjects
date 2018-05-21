I submit two folders, one for two seperate .py files (sender.py and receiver.py); one for only one .py file(jrip2), because I used to write seperate files for sending and receiving packets, but TA told me it should be merged to one file.

1. If you want to run two-files version, first run "python receiver.py -p 5001" then run "python sender.py -l 0.5 -p 7999 127.0.0.1:5001", then you can see the result in the terminal.

2. If you want to run one-file version:
a. open three terminals, and type the following three commands in three seperate terminal:
"./jrip2 -l 0.3 -p 7999 127.0.0.1:5001:10 127.0.0.1:5002:10"
"./jrip2 -l 0.3 -p 5001 127.0.0.1:7999:10 127.0.0.1:5002:10"
"./jrip2 -l 0.3 -p 5002 127.0.0.1:7999:10 127.0.0.1:5001:10"
Then run them at the same time, you will see the results.

b. After each host receives 100 packets from both destinations, it will generate a "<host_port>.txt" file to compute the goodput rate for each destination (Here I used (#distinct packets) divided by 100 to calculate the goodput).

Notes:
I append two seperate result files, one for two hosts, and another for three hosts. I set the loss rate 0.3 in both cases. In two hosts file, the goodput rates are 75/100 and 72/100 which are basically consistent to 70/100. For three hosts, the goodput rates for two hosts are close to 70/100, but the third host's goodput is a little lower than 70/100 (about 50/100). I think this is because this host spend more time than other ones in sending or receiving packets from both of them.