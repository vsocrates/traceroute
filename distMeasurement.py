#!/usr/bin/python

import socket

def main(file_name):
    initialData = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas vehicula, magna sed ullamcorper pulvinar, velit risus aliquet elit, at rhoncus arcu ipsum id felis. Nam laoreet id mauris eu porttitor. Proin et justo a nunc commodo mollis nec quis quam. Quisque mattis turpis a magna finibus, vel euismod enim sollicitudin. Curabitur dapibus rhoncus orci vel mollis. Vivamus aliquet mattis neque sit amet interdum. Praesent placerat, tellus vitae blandit lacinia, purus nisl vulputate nulla, a vulputate nibh sapien eu dui. Vestibulum sed tincidunt elit. Pellentesque sodales enim tortor, vel semper erat ultricies in. Aliquam vulputate feugiat facilisis. Morbi cursus ante quis ex scelerisque suscipit. Nulla fermentum lacus nec urna fringilla tincidunt. Aenean a iaculis nisl. In vitae tristique orci. Donec lacinia est consequat, dapibus lectus nec, mollis ante. Nullam mi odio, pulvinar in massa nec, lacinia ultrices sem. In bibendum ut tortor non posuere. Aliquam tincidunt lorem nec lorem pulvinar, et pharetra sapien tempor. Phasellus sodales enim hendrerit, pharetra tellus nec, auctor enim. Morbi lobortis justo sed nulla consectetur, id porta dui porttitor. Etiam eleifend arcu in consequat tincidunt. Nulla sit amet congue dui, fringilla blandit leo. Curabitur pulvinar purus eu dignissim aliquet. In eget quam et arcu rhoncus suscipit ut sit amet nibh. Donec et magna sed urna consectetur ultrices. Donec arcu lacus, fermentum eu leo et, laoreet ultricies diam. Done1"

    lines = [line.rstrip('\n') for line in file_name]

    port = 33434
    max_hops = 30
    icmp = socket.getprotobyname('icmp')
    udp = socket.getprotobyname('udp')
    ttl = 1
    while True:
        recv_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
        send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, udp)
        send_socket.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)
        
        recv_socket.bind(("", port))
        send_socket.sendto(initialData, (dest_name, port))
        curr_addr = None
        curr_name = None
        returnData = None
        try:
            returnData, curr_addr = recv_socket.recvfrom(1500)
            curr_addr = curr_addr[0]

        except socket.error:
            pass
        finally:
            send_socket.close()
            recv_socket.close()


if __name__ == "__main__":
    main('google.com')