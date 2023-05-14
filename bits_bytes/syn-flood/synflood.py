import struct
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

# Need to parse TCP header and IPV4 header
with open('synflood.pcap', 'rb') as f:
    pcap_header = f.read(24)
    magic_number, version_major, version_minor, thiszone, sigfigs, snaplen, network = struct.unpack('IHHIIII', pcap_header)
    assert(version_major == 2 and version_minor == 4)

    # read each packet
    while True:
        packet_header = f.read(16)
        print(packet_header)
        if packet_header == b'':
            break
        ts_sec, ts_usec, incl_len, orig_len = struct.unpack('IIII', packet_header)
        print(ts_sec, ts_usec, incl_len, orig_len)
        break
        raw_packet = f.read(incl_len)