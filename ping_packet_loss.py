#!/usr/bin/python
"""
The aim of this script is to send a certain number of icmp packets 
using ping commands with a packet defined size and return the percentage of packet loss
The Script is taking three arguments, first one being the target hostname/ip
The Second one (optional) is the number of packets to send, default to 10
The Third one (optional) is the size of the Packages, default to 3000
Written and maintained by Steve ESSO (https://github.com/stivesso)
"""
import platform, sys, subprocess

def check_args(lst):
    """The aim of this is to check that we have enough arguments"""
    if len(lst) < 2:
        print "This script needs at least a valid zone file path as argument"
        print "Its usage is", sys.argv[0], " destination_node <number_packet(default:10)> <packet_size:(default:3000)>"
        print "Number of Packet and Packet Size are optional"
        sys.exit("Insufficient Number of Arguments")


def ping_cmd(os_type,dest_node,number_packet = '10',size_packet = '3000'):
  """
  Functions which take as input an OS Type and a destination Name/IP
  optionally we can also add a number of Packet (default to 10)
  and Packet size (default to 3000)
  """
  if   os_type.lower() == "sunos": # Sun Systems
    return ["/usr/sbin/ping", "-s", dest_node, size_packet, number_packet]
  elif os_type.lower() == "linux": # Linux Systems
    return ["/bin/ping", "-q", "-c", number_packet, "-s", size_packet, dest_node]
  else: # Default to Linux Systems
    return ["/bin/ping", "-q", "-c", number_packet, "-s", size_packet, dest_node]
    
## Main function

# Check Number of Arguments
check_args(sys.argv)

# Get the ping commands
myping =  ping_cmd(platform.system(),*sys.argv[1:])

# Run and get the ping response
ping_response  = subprocess.Popen(myping, stdout=subprocess.PIPE).stdout.read()
ping_line_loss = [line for line in ping_response.split("\n") if "loss" in line.lower()][0].split(",")
ping_loss      = [ch for ch in ping_line_loss if "loss" in ch.lower()][0]
print ping_loss.split()[0].strip('%')
