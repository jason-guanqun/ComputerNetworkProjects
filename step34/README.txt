Step 3:
1. I used the same structure as piazza says to store the packets: dict in dict.
2. First initialize router's own routing table according to the command line. (I set -1 (infinity) to neighbours' cost if I don't know its routing table) 
3. Set a daemon to keep sending the routing table to my neighbours every 10s.  
4. Each time I received a packet first check if its a JRIP type packet then doing the update.
5. If my routing table is updated then send it to all my neighbours immediately.
If one wants to try the topology with 4 nodes, just type something like "./jrip34 -p 5004 127.0.0.1:7999:50 127.0.0.1:5003:4" according to your neighbours then the updated routing table will be printed in the terminal.

PS: I tried my own way to update the routing table: Assume I'm node A and I received a routing table from node B. I only replace the node B vector in my table with the new vector send by B (which means not considering other vectors in routing table B). And I only update my A vector according to the new B vector in the following way: Iterate the new B vector and check each address addr, if addr not in A vector, then A vector append this addr with value c(A, B)+ D_B(addr); if addr in A vector and value c(A, B) + D_B(addr) is less than its value, then update A[addr]. That's why I only need few lines of code to update each routing table.

Step 4:

1. jtraceroute file sends request for routing path. It will send the request every 5s until it gets a response from the destination then print the path and exit.
2. For jrip34, if it received a TRACE type packet, it will invoke the proc_trace function and do the update for trace list and send it to the next hop.
The command line is like "./jtraceroute -p 4321 127.0.0.1:7999 127.0.0.1:5004". I did three experiments, two for 4 nodes and one for 5 nodes which are attached in seperate folders