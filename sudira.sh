#!/bin/bash

# Function to display help
function show_help {
    echo "Usage: ./sudira.sh -d domain -s api_key"
    echo ""
    echo "Options:"
    echo "  -d domain   Specify the domain to enumerate subdomains for."
    echo "  -s api_key  Provide the API key for shosubgo."
    echo "  -h          Show this help message."
    exit 1
}

# Parse command line arguments
while getopts "d:s:h" opt; do
    case $opt in
        d) domain="$OPTARG" ;;
        s) api_key="$OPTARG" ;;
        h) show_help ;;
        *) show_help ;;
    esac
done

# Check if domain and api_key are provided
if [ -z "$domain" ] || [ -z "$api_key" ]; then
    show_help
fi

# Run subdomain enumeration tools
subfinder -d "$domain" -all -o domain1.txt
assetfinder "$domain" -subs-only > domain2.txt
sublist3r -d "$domain" -o domain3.txt
shosubgo -d "$domain" -s "$api_key" > domain4.txt

# Combine results and remove duplicates
cat domain1.txt domain2.txt domain3.txt domain4.txt | anew > final.txt

# Filter for active domains
httpx -mc 200 -l final.txt -o aktif.txt

# Remove lines from aktif.txt that do not contain the domain
grep -i "$domain" aktif.txt > temp.txt && mv temp.txt aktif.txt

# Clean up intermediate files
rm domain1.txt domain2.txt domain3.txt domain4.txt final.txt

echo "Subdomain enumeration completed. Active domains saved in aktif.txt."
