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

    # Extract Flags
    flags_match = re.search(r"flags:\s*([^\s]+)", block)
    if flags_match:
        row["Flags"] = flags_match.group(1)
    # Extract Query size
    query_size_match = re.search(r"Query size:\s*(\d+)", block)
    if query_size_match:
        row["Query size"] = query_size_match.group(1)
    # Extract Response size
    response_size_match = re.search(r"Response size:\s*(\d+)", block)
    if response_size_match:
        row["Response size"] = response_size_match.group(1)
    # Extract # of Answers
    answers_match = re.search(r"ANSWER:\s*(\d+)", block)
    if answers_match:
        row["# of Answers"] = answers_match.group(1)
    # Extract # of Authority RRs
    authority_match = re.search(r"AUTHORITY:\s*(\d+)", block)
    if authority_match:
        row["# of Authority RRs"] = authority_match.group(1)
    # Extract # of Additional RRs
    additional_match = re.search(r"ADDITIONAL:\s*(\d+)", block
    )
    if additional_match:
        row["# of Additional RRs"] = additional_match.group(1)
    # Check for Truncated flag
    if "truncated" in block.lower():
        row["Truncated?"] = "Yes"
    data.append(row)
    