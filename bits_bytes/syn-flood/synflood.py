import struct
from collections import defaultdict
""" Global header:
 typedef struct pcap_hdr_s {
          guint32 magic_number;   /* magic number */
          guint16 version_major;  /* major version number */
          guint16 version_minor;  /* minor version number */
          gint32  thiszone;       /* GMT to local correction */
          guint32 sigfigs;        /* accuracy of timestamps */
          guint32 snaplen;        /* max length of captured packets, in octets */
          guint32 network;        /* data link type */
  } pcap_hdr_t;
"""

""" Each packet:
 typedef struct pcaprec_hdr_s {
          guint32 ts_sec;         /* timestamp seconds */
          guint32 ts_usec;        /* timestamp microseconds */
          guint32 incl_len;       /* number of octets of packet saved in file */
          guint32 orig_len;       /* actual length of packet */
  } pcaprec_hdr_t;
  
  each packet is immediately followed by the raw packet data of length incl_len
"""
with open('synflood.pcap', 'rb') as f:
    pcap_header = f.read(24)
    magic_number, version_major, version_minor, thiszone, sigfigs, snaplen, network = struct.unpack('<IHHIIII', pcap_header)
    assert version_major == 2 and version_minor == 4

    unacked = defaultdict(int)
    acked = 0
    # read each packet
    while True:
        packet_header = f.read(16)
        if packet_header == b'':
            break
        ts_sec, ts_usec, incl_len, orig_len = struct.unpack('<IIII', packet_header)
        packet = f.read(incl_len)
        link_layer_header = packet[:4]
        assert struct.unpack('I', link_layer_header)[0] == 2 # ipv4 (24, 28, or 30 for ipv6)
        internet_header_length = (struct.unpack('H', packet[4:6])[0] & 0b00001111) << 2 # gives number of 32-bit words so multiply by 4
        assert internet_header_length == 20 # if this is false, then more options were included in the header
        src_port, dst_port, seq_num, ack_num, offset_reserved, flags, window_size, checksum, urgent_pointer = struct.unpack('>HHIIBBHHH', packet[24:44])
        syn = flags & 0b00000010 != 0
        ack = flags & 0b00010000 != 0
        print(f"{src_port} -> {dst_port}: ", syn, ack)
  

        if src_port == 80:
            # this is a response from the server
            assert syn and ack
            acked += 1
        else:
            # this is a request from the client
            if syn:
              unacked[src_port] = seq_num
            elif ack:
                del unacked[src_port]
                print(f"src {src_port} actually completed the handshake!")
        print(f"{len(unacked)} unacked handshakes, {acked} acked")
        # break