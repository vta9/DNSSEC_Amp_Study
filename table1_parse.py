import re
import csv

input_file = "dnskey_results.txt"
#Table 1 is a csv of the 1k domains resolved at 8.8.8.8 and their high level DNSKEY results (e.g. whether they have DNSSEC, how many keys, etc.)
output_file = "table1.csv"

fields = [
    "Domain",
    "Flags",
    "Query size",
    "Response size",
    "# of Answers",
    "# of Authority RRs",
    "# of Additional RRs",
    "Truncated?"
]

data = []

with open(input_file, "r") as f:
    content = f.read()

# Split by domain headers (=== domain ===)
domains_blocks = re.split(r"===\s*(.*?)\s*===", content)

for i in range(1, len(domains_blocks), 2):
    domain = domains_blocks[i].strip()
    block = domains_blocks[i+1]

    # Initialize row
    row = {
        "Domain": domain,
        "Flags": "",
        "Query size": "",
        "Response size": "",
        "# of Answers": "",
        "# of Authority RRs": "",
        "# of Additional RRs": "",
        "Truncated?": "No"
    }

    # Flags line: ;; flags: qr rd ra ad; QUERY: 1, ANSWER: 2, AUTHORITY: 0, ADDITIONAL: 0
    flags_match = re.search(
        r";; flags: (.*?); QUERY: (\d+), ANSWER: (\d+), AUTHORITY: (\d+), ADDITIONAL: (\d+)", block
    )
    if flags_match:
        row["Flags"] = flags_match.group(1).strip()
        row["# of Answers"] = int(flags_match.group(3))
        row["# of Authority RRs"] = int(flags_match.group(4))
        row["# of Additional RRs"] = int(flags_match.group(5))

    # MSG SIZE line: ;; MSG SIZE  rcvd: 754
    msg_size_match = re.search(r";; MSG SIZE\s+rcvd:\s*(\d+)", block)
    if msg_size_match:
        row["Response size"] = int(msg_size_match.group(1))

    #Query size 
    query_size_match = re.search(r";; QUERY SIZE:\s*(\d+)", block)
    if query_size_match:
        row["Query size"] = int(query_size_match.group(1))

    # Truncated?
    if "Truncated, retrying in TCP mode" in block:
        row["Truncated?"] = "Yes"

    data.append(row)

    # write to CSV
with open(output_file, "w", newline="") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fields)
    writer.writeheader()
    for row in data:
        writer.writerow(row)
print(f"Finished! Table 1 saved in {output_file}")

