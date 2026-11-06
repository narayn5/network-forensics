import sys, pandas as pd
from elasticsearch import Elasticsearch, helpers

csv_file, case_name = sys.argv[1], sys.argv[2]
df = pd.read_csv(csv_file)
df.columns = [c.replace(".", "_") for c in df.columns]
df["@timestamp"] = pd.to_datetime(df["frame_time_epoch"], unit="s").dt.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
for col in ["tcp_flags_reset", "tcp_analysis_retransmission",
            "tcp_analysis_zero_window", "tcp_analysis_duplicate_ack"]:
    df[col] = df[col].fillna(0).astype(int)
df["case"] = case_name
df = df.where(df.notna(), None)

es = Elasticsearch("http://localhost:9200")
actions = ({"_index": "tcp-packets", "_source": r} for r in df.to_dict("records"))
success, errors = helpers.bulk(es, actions, raise_on_error=False)
print("indexed:", success, "failed:", len(errors))
for e in errors[:3]:
    print(e)
print("done")
