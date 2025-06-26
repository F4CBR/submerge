#!/usr/bin/env python3

import subprocess
import argparse
import os

def run_command(command, output_file=None):
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        if output_file:
            with open(output_file, "w") as f:
                f.write(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"[!] Command failed: {command}\n{e}")

def main():
    parser = argparse.ArgumentParser(description="All-in-One Subdomain Recon Tool (Python Version)")
    parser.add_argument("-d", "--domainfile", required=True, help="File containing list of domains")
    parser.add_argument("-s", "--shosubgo_key", required=True, help="API key for shosubgo")

    args = parser.parse_args()

    if not os.path.isfile(args.domainfile):
        print(f"[!] File not found: {args.domainfile}")
        return

    with open(args.domainfile, "r") as f:
        domains = [line.strip() for line in f if line.strip()]

    for domain in domains:
        print(f"🔍 Processing domain: {domain}")
        base = domain.replace("://", "").replace("/", "").replace(":", "_")

        # Run tools
        run_command(f"subfinder -d {domain} -all -silent", "domain1.txt")
        run_command(f"assetfinder {domain} -subs-only", "domain2.txt")
        run_command(f"sublist3r -d {domain} -o domain3.txt > /dev/null 2>&1", None)
        run_command(f"shosubgo -d {domain} -s {args.shosubgo_key}", "domain4.txt")

        # Combine and dedupe
        combined = set()
        for fname in ["domain1.txt", "domain2.txt", "domain3.txt", "domain4.txt"]:
            if os.path.exists(fname):
                with open(fname, "r") as f:
                    combined.update(line.strip() for line in f if line.strip())
        with open("final.txt", "w") as f:
            f.write("\n".join(sorted(combined)))

        # Filter live
        run_command("httpx -silent -mc 200 -l final.txt -o temp_live.txt")
        with open("temp_live.txt", "r") as f:
            lines = [line for line in f if domain in line.lower()]
        with open(f"{base}-aktif.txt", "w") as f:
            f.write("".join(lines))

        print(f"✅ Saved to {base}-aktif.txt\n")

        # Clean up
        for fname in ["domain1.txt", "domain2.txt", "domain3.txt", "domain4.txt", "final.txt", "temp_live.txt"]:
            if os.path.exists(fname):
                os.remove(fname)

    print("🎉 All domains processed.")

if __name__ == "__main__":
    main()
