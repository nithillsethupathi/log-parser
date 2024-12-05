import random
import time
import ipaddress
import os
'''
Function to generate additional flow logs if needed
'''


def generate_logs(num_logs, file_name):
    interface = ["eni-4d3c2b1a", "eni-8d3c2b1b",
                 "eni-4d3c2b9a", "abc-4d3c2b1a", "gbc-4d3c2b1a"]

    with open(file_name, "w") as f:
        for _ in range(num_logs):
            version = random.randrange(1, 5)
            account_id = random.randrange(1000000, 99999999)
            interface_id = random.choice(interface)
            src_addr = generate_ip()
            dst_addr = generate_ip()
            src_port = random.randrange(1, 9999)
            dst_port = random.randrange(1, 9999)
            protocol = random.choice([1, 6, 8, 9, 17])
            packets = random.randrange(1, 100)
            bytes_transfer = str(random.randrange(100, 1000))
            start = time.time()
            end = time.time()
            action = random.choice(["ACCEPT", "REJECT"])
            log = f"{version} {account_id} {interface_id} {src_addr} {dst_addr} {src_port} {dst_port} {protocol} {packets} {bytes_transfer} {start} {end} {action}\n"
            f.write(log)


def generate_ip():
    return str(ipaddress.IPv4Address(int.from_bytes(os.urandom(4), byteorder="big")))


if __name__ == "__main__":
    generate_logs(100000, file_name='resources/logs_2.log')
    print("Logs have been generated")
