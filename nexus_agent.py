import json
import sys
from collections import defaultdict
from kubernetes import client, config

def get_k8s_errors():
    try:
        config.load_incluster_config()
        v1 = client.CoreV1Api()
        pods = v1.list_namespaced_pod("spring-petclinic")
        errors = []
        for pod in pods.items:
            statuses = pod.status.container_statuses or []
            for container in statuses:
                if container.state.waiting:
                    reason = container.state.waiting.reason
                    errors.append({
                        "service": pod.metadata.name,
                        "level": "service" if "Image" in reason else "app",
                        "error": reason
                    })
        return errors
    except Exception as e:
        return [{"service": "k8s-api", "level": "system", "error": str(e)}]

def get_correlated_traces():
    k8s_traces = get_k8s_errors()
    deduped = {}
    for trace in k8s_traces:
        key = (trace["service"], trace["error"])
        if key not in deduped:
            deduped[key] = trace
    
    result = defaultdict(list)
    for val in deduped.values():
        result[val["level"]].append({"service": val["service"], "error": val["error"]})
    return dict(result)

if __name__ == "__main__":
    print(json.dumps(get_correlated_traces(), indent=2))
    sys.stdout.flush()
