import requests

# Define URLs for each tracing tool
# Use ClusterIP of the services
PARCA_URL = "http://10.0.78.82:7070/api/traces"
PIXIE_URL = "http://10.0.75.156:50300/v1/traces"
OTEL_URL = "http://10.0.68.10:4318/traces"

def fetch_traces(url, name):
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        print(f"Fetched {len(data)} traces from {name}")
        return data
    except Exception as e:
        print(f"[ERROR] Could not fetch traces from {name}: {e}")
        return []

def main():
    parca_traces = fetch_traces(PARCA_URL, "Parca")
    pixie_traces = fetch_traces(PIXIE_URL, "Pixie")
    otel_traces = fetch_traces(OTEL_URL, "OpenTelemetry")

    all_traces = parca_traces + pixie_traces + otel_traces
    unique_traces = {t['id']: t for t in all_traces if 'id' in t}

    print(f"\nTotal traces fetched: {len(all_traces)}")
    print(f"Unique traces after deduplication: {len(unique_traces)}")

if __name__ == "__main__":
    main()
