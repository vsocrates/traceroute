#!/usr/bin/python

import socket
import sys
import struct 
import select
import time 
import sys
from matplotlib import use
use('Agg')
from matplotlib import pyplot
from pylab import *
from numpy import *

def main():
    initialData = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas vehicula, magna sed ullamcorper pulvinar, velit risus aliquet elit, at rhoncus arcu ipsum id felis. Nam laoreet id mauris eu porttitor. Proin et justo a nunc commodo mollis nec quis quam. Quisque mattis turpis a magna finibus, vel euismod enim sollicitudin. Curabitur dapibus rhoncus orci vel mollis. Vivamus aliquet mattis neque sit amet interdum. Praesent placerat, tellus vitae blandit lacinia, purus nisl vulputate nulla, a vulputate nibh sapien eu dui. Vestibulum sed tincidunt elit. Pellentesque sodales enim tortor, vel semper erat ultricies in. Aliquam vulputate feugiat facilisis. Morbi cursus ante quis ex scelerisque suscipit. Nulla fermentum lacus nec urna fringilla tincidunt. Aenean a iaculis nisl. In vitae tristique orci. Donec lacinia est consequat, dapibus lectus nec, mollis ante. Nullam mi odio, pulvinar in massa nec, lacinia ultrices sem. In bibendum ut tortor non posuere. Aliquam tincidunt lorem nec lorem pulvinar, et pharetra sapien tempor. Phasellus sodales enim hendrerit, pharetra tellus nec, auctor enim. Morbi lobortis justo sed nulla consectetur, id porta dui porttitor. Etiam eleifend arcu in consequat tincidunt. Nulla sit amet congue dui, fringilla blandit leo. Curabitur pulvinar purus eu dignissim aliquet. In eget quam et arcu rhoncus suscipit ut sit amet nibh. Donec et magna sed urna consectetur ultrices. Donec arcu lacus, fermentum eu leo et, laoreet ultricies diam. Done1"

    with open('targets.txt') as f:
        content = f.readlines()

    print(len(content))
    
    port = 33434
    max_hops = 30
    icmp = socket.getprotobyname('icmp')
    udp = socket.getprotobyname('udp')
    ttl = 32
    ipAdd = 0;
    tryCount = 1;

    while ipAdd < (len(content)):
        print '\n'
        print '%i' % ipAdd
        recv_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
        send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, udp)
        send_socket.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)
        recv_socket.settimeout(5)
        
        recv_socket.bind(("", port))
        t0 = time.time()
        send_socket.sendto(initialData, (str(content[ipAdd]), port))
        curr_addr = None
        curr_name = None
        returnData = None
        try:
            # inputs = [send_socket]
            # outputs = [recv_socket]
            # readable, writable, exception = select.select(inputs, outputs, inputs)
            # for s in readable:
            #     returnData, curr_addr = s.recvfrom(1500)
            #     print(returnData)
            #     if returnData:
            #         print("Read data!")
            #     else:
            #         inputs.remove(s)
            #         s.close()
            returnData, curr_addr = recv_socket.recvfrom(1500)
            
            t1 = time.time()
            totalTime = round((t1 - t0) * 1000, 3)
            print("The time elapsed was: " + str(totalTime) + " ms")
            TTL, protocol, src_ip, dest_ip = parseIPHeader(returnData,28)

            IPHeaderLength(returnData,0)
            ICMPHeader(returnData, 20)

            ipAdd = ipAdd + 1

        
        except socket.error:
            if tryCount > 2:
                tryCount = 1
                print("Gave up after 3 tries")
                ipAdd = ipAdd + 1
                continue
            else:
                tryCount = tryCount + 1
                continue
            
        finally:
            send_socket.close()
            recv_socket.close()
            ttl_list.append(TTL)
            rtt_list.append(totalTime)
            totalTime = 0;



def IPHeaderLength(byte_array,initialMark):
    stringRegex = "!xxH"
    datagramLength = struct.unpack(stringRegex, byte_array[initialMark:initialMark + 4])
    print("The total length is: %i" % datagramLength)
    print("The original length was: %i" % (datagramLength[0] - 28))


def parseIPHeader(byte_array, initialMark):
    stringRegex = "!xxxxxxxxBBxx4s4s"
    TTL, protocol, src_ip, dest_ip = struct.unpack(stringRegex, byte_array[initialMark:initialMark + 20])
    print("The current TTL is: %d " %  TTL)
    print("The protocol is: %d" %  protocol)
    src_ip_string = socket.inet_ntoa(src_ip)
    dest_ip_string = socket.inet_ntoa(dest_ip)
    print("The source IP is: " + src_ip_string)
    print("The destination IP is: " + dest_ip_string)
    return TTL, protocol, src_ip, dest_ip

def ICMPHeader(byte_array, initialMark):
    stringRegex = "!BBxx"
    icmp_type, icmp_code = struct.unpack(stringRegex, byte_array[initialMark:initialMark + 4])
    print("The ICMP Type is: %i" % icmp_type)
    print("The ICMP Code is: %i" % icmp_code)

if __name__ == "__main__":
    main()

def plotGraph(xData, yData):
    pyplot.figure()
    #pyplot.errorbar(x, m, yerr=s) # Plot lines
    pyplot.plot(xData, yData, ".") # Plot markers
    xlim((min(x) - (0.15 * min(xData))), max(xData) + (0.15 * min(xData))) # Adjust x-axis limits
    xlabel('Size of Array (N)')
    ylabel('Time (sec)')
    title(filename)
    savefig(filename + '.png')
