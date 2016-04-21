#!/usr/bin/python

import socket
import sys
import struct 
import select
import time 
import sys
import csv 
import traceback 


def main():
    initialData = "Gastropub forage chillwave, farm-to-table locavore scenester mumblecore chia. Master cleanse truffaut lumbersexual brunch. Hashtag mlkshk twee, flexitarian four dollar toast narwhal kogi. Farm-to-table tilde pork belly, slow-carb lumbersexual cliche hoodie shoreditch whatever hella. Bicycle rights iPhone try-hard, paleo vice yuccie flexitarian heirloom skateboard cold-pressed kombucha tofu whatever. +1 before they sold out post-ironic, affogato austin jean shorts echo park actually heirloom bicycle rights drinking vinegar. Photo booth actually mlkshk listicle. Kitsch raw denim semiotics slow-carb DIY, chia hashtag artisan literally forage messenger bag kinfolk. Venmo chillwave fingerstache, williamsburg knausgaard butcher flannel pinterest paleo +1 gochujang. Raw denim affogato marfa ethical freegan, celiac fanny pack church-key hashtag mixtape blue bottle pabst flannel. Wayfarers cardigan paleo, kombucha drinking vinegar celiac trust fund helvetica. Affogato tattooed hella mlkshk knausgaard, meh kickstarter shoreditch celiac migas austin cronut. Portland occupy thundercats yr pug tattooed before they sold out, paleo fap gastropub dreamcatcher wayfarers vice. Keffiyeh skateboard pabst, pop-up semiotics you probably haven't heard of them church-key artisan.Ethical photo booth shoreditch, blue bottle tattooed everyday carry schlitz yr +1 blog scenester thundercats. Cliche flexitarian man bun, disrupt kombucha pabst bicycle rights. Mumblecore synth twee, Done"

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
    csv_count = 0;
    residualTTL = 0

    f = open('output.csv', 'w')
    try:
        writer = csv.writer(f)
        writer.writerow( ('IP Address' , 'Hops', 'RTT', 'GeoDistance') )
        while ipAdd < (len(content)):
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
              TTL, protocol, src_ip_string, dest_ip_string  = parseIPHeader(returnData,28)

              IPHeaderLength(returnData,0)
              icmp_type, icmp_code = ICMPHeader(returnData, 20)

              ipAdd = ipAdd + 1

              if icmp_type == 3 & icmp_code == 3:
                  residualTTL = 32 - TTL
                  writer.writerow( (dest_ip_string,residualTTL, totalTime) )
                  csv_count += 1
                  if csv_count > 9:
                      break
              
              print '\n'   
            
            
          except socket.error:
              if tryCount > 2:
                  tryCount = 1
                  print("Gave up after 3 tries")
                  ipAdd = ipAdd + 1
                  print '\n'
                  continue
              else:
                  tryCount = tryCount + 1
                  continue

          finally:
              send_socket.close()
              recv_socket.close()
    except:
        print("Oh no!")
        traceback.print_exc()
    finally:
        f.close()    
def IPHeaderLength(byte_array,initialMark):
    stringRegex = "!xxH"

    datagramLength = struct.unpack(stringRegex, byte_array[initialMark:initialMark + 4])
    print("The total length is: %i" % datagramLength[0])
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
    return TTL, protocol, src_ip_string, dest_ip_string

def ICMPHeader(byte_array, initialMark):
    stringRegex = "!BBxx"
    icmp_type, icmp_code = struct.unpack(stringRegex, byte_array[initialMark:initialMark + 4])
    print("The ICMP Type is: %i" % icmp_type)
    print("The ICMP Code is: %i" % icmp_code)
    return icmp_type, icmp_code

if __name__ == "__main__":
    main()
