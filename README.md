# LAB 1 — RPC on AWS EC2 (Distributed Computing)

## Setup
Two EC2 instances (Amazon Linux 2):
- rpc-server-node (port 5000 open in Security Group)
- rpc-client-node

## Run server (on server EC2)
```bash
python3 server.py

Run client (on client EC2)

Edit SERVER_IP in client.py to the server public IP, then:

python3 client.py

