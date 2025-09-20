from kamene.all import ARP, Ether, sr1,sendp
import netifaces # check if a interface exists

import time
import argparse
import os

def send_garp_conflict(target_ip, interface, count=3):
    """
    Send Gratuitous ARP packets to simulate an IP conflict on the network.
    """
    # Check if the interface exists
    if interface not in netifaces.interfaces():
        print(f"Interface {interface} does not exist.")
        os.exit(1)

    # Build the Ethernet frame, target is L2 broadcast
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")

   
    # Build the gratuitous ARP packet
    # op=1 means ARP request, psrc and pdst are the same for conflict with target_ip
    arp = ARP(op=1, psrc=target_ip, pdst=target_ip)
    
    # Build the frame
    frame = ether / arp
    frame.show()
    
    # Send the frame multiple times
    for i in range(count):
        sendp(frame, iface=interface, verbose=1)
        time.sleep(10)
        print(f"Sent {i+1}/{count} GARP packets to {target_ip} on {interface}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Send GARP packets to simulate IP conflict")
    parser.add_argument("-ip", "--target_ip", required=True, help="Target IP address to simulate conflict")
    parser.add_argument("-int", "--interface", required=True, help="Network interface to send packets on")
    parser.add_argument("-c","--count", type=int, default=3, help="Number of GARP packets to send (default: 3)")
    
    args = parser.parse_args()
    
    send_garp_conflict(args.target_ip, args.interface, args.count)