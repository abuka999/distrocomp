import socket
import json
import time

HOST = "0.0.0.0"
PORT = 5000

def handle_method(method: str, params: dict):
    if method == "add":
        return params["a"] + params["b"]
    if method == "reverse_string":
        return params["s"][::-1]
    if method == "get_time":
        return time.ctime()
    raise ValueError("Unknown method")

def main():
    print(f"[SERVER] Listening on {HOST}:{PORT}")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(5)

        while True:
            conn, addr = s.accept()
            with conn:
                data = conn.recv(4096)
                if not data:
                    continue

                try:
                    req = json.loads(data.decode("utf-8"))
                    request_id = req.get("request_id")
                    method = req.get("method")
                    params = req.get("params", {})

                    print(f"[SERVER] req_id={request_id} method={method} params={params}")

                    # Failure demo: deliberately slow down
                    time.sleep(5)

                    result = handle_method(method, params)
                    resp = {"request_id": request_id, "result": result, "status": "OK"}

                except Exception as e:
                    resp = {"request_id": "unknown", "error": str(e), "status": "ERROR"}

                conn.sendall(json.dumps(resp).encode("utf-8"))

if __name__ == "__main__":
    main()
