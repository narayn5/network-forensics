# TCP Triage

Find out why a network connection is slow or broken by reading a packet capture, then see the key numbers on a Kibana dashboard.

## What this project does

1. Open a packet capture (`.pcap`) in Wireshark
2. Write up all observations using existing Wireshark analysis
3. Export a small set of fields to a CSV file.
4. Load the CSV into Elasticsearch with a short Python script.
5. View the results in Kibana: retransmissions, zero window events, resets, handshake time, and window size.

## What I looked for

| What | Wireshark filter | What it can mean |
| --- | --- | --- |
| Any TCP warning | `tcp.analysis.flags` | Something unusual happened. Check what. |
| Resent data | `tcp.analysis.retransmission` | Packet loss or delay |
| Receiver full | `tcp.analysis.zero_window` | The receiving app or host is too slow |
| Repeated ACKs | `tcp.analysis.duplicate_ack` | A packet may be missing |
| Connection killed | `tcp.flags.reset == 1` | Closed port, firewall, or app abort |
| Slow handshake | `tcp.analysis.initial_rtt` | High latency between hosts |
| Pauses | `tcp.time_delta > 0.03` | The sender or receiver is waiting on something |

Sample captures come from the [Wireshark Sample Captures page](https://wiki.wireshark.org/SampleCaptures).

## How to run it

You need Wireshark, Docker Desktop, and Python 3.

**1. Start Elasticsearch and Kibana**

```
docker compose up -d
```

Wait 2 to 3 minutes. Then check:
- Elasticsearch: http://localhost:9200
- Kibana: http://localhost:5601

**2. Install the Python libraries**

```
pip install pandas "elasticsearch>=8,<9"
```

Use version 8 of the `elasticsearch` library to match the server. Version 9 gives a media-type error.

**3. Export a capture to CSV**

In Wireshark, add these as columns (Custom type) and name each column with the field name:

`frame.time_epoch`, `ip.src`, `ip.dst`, `tcp.stream`, `tcp.window_size`, `tcp.flags.reset`, `tcp.analysis.retransmission`, `tcp.analysis.zero_window`, `tcp.analysis.duplicate_ack`, `tcp.analysis.initial_rtt`

Then use **File > Export Packet Dissections > As CSV**. Save it in the `exports` folder.

**4. Load it into Elasticsearch**

```
python load.py exports/capture1.csv case1
```

**5. Open Kibana**

1. Create a data view named `tcp-packets` with `@timestamp` as the time field.
2. Open the dashboard called **TCP Triage**.
3. **Set the time range to match the capture.** Packet captures keep their original dates, so the default "Last 15 minutes" will show nothing.

## Dashboard panels

- Retransmissions over time
- Handshake round-trip time
- Zero window count
- Resets by host
- Top problem flows by stream

## What I learned

- A filter that returns nothing is still a result. It rules out a cause.
- Flagged does not mean broken. I check the count, the timing, and what happens around the packets.
- A capture with no errors can still be slow, and the time gaps between packets show why.

## Important Note

- The dashboard uses a few fields per packet, not full packet detail.
- Some Wireshark sample files have truncated packets or missing segments, which can add warnings that are not real network problems.