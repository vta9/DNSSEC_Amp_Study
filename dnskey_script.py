import subprocess

# File containing domains
domains_file = "domains.txt"
output_file = "dnskey_results.txt"

# Resolver to query
resolver = "8.8.8.8"

# Dig options
dig_options = ["+stats", "+qr", "+bufsize=4096"]  # You can adjust buffer size

with open(domains_file, "r") as f:
    domains = [line.strip() for line in f if line.strip()]

with open(output_file, "w") as out:
    for domain in domains:
        out.write(f"=== {domain} ===\n")
        try:
            # Build the dig command
            cmd = ["dig", f"@{resolver}", "DNSKEY", domain] + dig_options
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            out.write(result.stdout + "\n")
        except subprocess.CalledProcessError as e:
            out.write(f"Error querying {domain}: {e}\n\n")

print(f"Finished! Results saved in {output_file}")
