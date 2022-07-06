import csv
import collections


class Node:
    def __init__(self):
        self.val = set()
        self.children = collections.defaultdict(Node)


# read and prepare entries
print("read entries")
entries = []
with open('geoip2-ipv4.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        network = row["network"].split("/")

        # convert ip address to bytes
        ip = network[0]
        mask = int(network[1])
        nums = ip.split(".")
        ip_byte_list = map(lambda x: bin(int(x)).lstrip('0b'), nums)
        ip_bits = "".join(ip_byte_list)[:mask]

        entries.append({
            "prefix": ip_bits,
            "country": row["country_name"]
        })


# init trie
root = Node()

# build trie
print("build trie")
for entry in entries:
    cur = root
    for bit in entry["prefix"]:
        cur.children[bit].val.add(entry["country"])
        cur = cur.children[bit]

# test ip
test_ip = "1001001001001"
print(f"test ip {test_ip}")
cur = root
for bit in test_ip:
    next = cur.children[bit]
    if len(next.val) == 0:
        break
    else:
        cur = next

print(f"{cur.val}")