# NFS Bad Stalls

## Symptoms

Stair case patterns

## Filters and Observations

- tcp.analysis.flags - 35 red flags meaning there have been 35 abnormal events in this packets capture
- tcp.analysis.retransmission - no signal loss reported (0 packets returned)
- tcp.analysis.zero_window - no problems with buffer being full and sender must stop sending
- tcp.flags.reset == 1 - no abrupt connection kills

## Root Cause Analysis

No signal loss reported, no problems with buffer being full and sender must stop sending, no abrupt connection kills

## Suggested Fix

Not applicable
