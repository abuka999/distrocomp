import socket
import json
import uuid
import time

SERVER_IP = "3.239.70.246"
PORT = 5000

TIMEOUT_SEC = 8
MAX_RETRIES = 3

def rpc_call(method: str, params: dict):
    request_id = str(uuid.uuid4())

    req = {
        "request_id": request_id,
        "method": method,
        "params": params,
        "timestamp": time.time()
    }

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            print(f"[CLIENT] Attempt {attempt}/{MAX_RETRIES} req_id={request_id}")
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(TIMEOUT_SEC)
                s.connect((SERVER_IP, PORT))
                s.sendall(json.dumps(req).encode("utf-8"))
                data = s.recv(4096)

            resp = json.loads(data.decode("utf-8"))
            return resp

        except socket.timeout:
            print("[CLIENT] Timeout -> retrying...")
        except Exception as e:
            print(f"[CLIENT] Error: {e} -> retrying...")

    return {"request_id": request_id, "status": "ERROR", "error": "No response after retries"}

def main():
    resp = rpc_call("add", {"a": 5, "b": 7})
    print("[CLIENT] Response:", resp)

if __name__ == "__main__":
    main()
