
# Observations

- The packet capture is between two endpoints all within the same subnet, within the same LAN. 172.16.0.1 to 172.16.0.101.
- There are two conversations that have happened in this packet capture.
- This packet capture is 100% TCP traffic that consists of transporting HTTP packets along with certificate management related traffic
- Two thirds of packets are averaging less than 100 bytes (small control frames), which would indicate traffic is mostly about exchanging header data and few data packets that are between 600 and 1300 bytes, may be carrying certificates payload.
- There have been few warnings relating to BER Errors.
- No connection failure detected in this capture. 
- No packet loss has happened and no retransmissions have taken place. 
- No out of order acknowledgments have happened.
- No stoppage of transfers have happened.
- 3 TCP connections appears to have been closed.
