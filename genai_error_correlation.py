import json
from collections import defaultdict

# Dummy data sources (replace with API calls to Parca, Pixie, OpenTelemetry)
parca_traces = [
    {"service": "customers", "level": "app", "error": "NullPointer"},
    {"service": "mysql", "level": "system", "error": "DiskFull"}
]

pixie_traces = [
    {"service": "customers", "level": "app", "error": "NullPointer"},
    {"service": "discovery", "level": "service", "error": "TimeoutError"}
]

otel_traces = [
    {"service": "customers", "level": "app", "error": "NullPointer"},
    {"service": "mysql", "level": "system", "error": "DiskFull"}
]

# Merge all traces
all_traces = parca_traces + pixie_traces + otel_traces

# Deduplicate errors by service+error
deduped = defaultdict(dict)
for trace in all_traces:
    key = (trace["service"], trace["error"])
    if key not in deduped:
        deduped[key] = trace

# Correlate levels
result = defaultdict(list)
for val in deduped.values():
    result[val["level"]].append({"service": val["service"], "error": val["error"]})

# Print summary
print(json.dumps(result, indent=2))
