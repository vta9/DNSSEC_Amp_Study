import subprocess
import csv

domains_file = "tranco_ZWLLG.csv"
output_file = "dnskey_results_1M.txt"

resolver = "8.8.8.8"
dig_options = ["+stats", "+qr", "+bufsize=4096"]

# Count total lines for progress tracking (optional but nice)
with open(domains_file, "r") as f:
    total = sum(1 for _ in f)

processed = 0

with open(domains_file, "r") as f, open(output_file, "w") as out:
    reader = csv.reader(f)

    for row in reader:
        if len(row) < 2:
            continue

        processed += 1

        number = row[0].strip()
        domain = row[1].strip()

        out.write(f"=== {number}, {domain} ===\n")

        try:
            cmd = ["dig", f"@{resolver}", "DNSKEY", domain] + dig_options
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            out.write(result.stdout + "\n")
        except subprocess.CalledProcessError as e:
            out.write(f"Error querying {number}, {domain}: {e}\n\n")

        # Print progress every 1000 domains
        if processed % 1000 == 0:
            percent = (processed / total) * 100
            print(f"Processed {processed}/{total} ({percent:.2f}%)")

print(f"Finished! Results saved in {output_file}")