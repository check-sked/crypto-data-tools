import requests
import csv
from datetime import datetime

# Input protocol to observe
Protocol = "Aave"

# Make a request to the endpoint
try:
    # Send GET request to endpoint
    response = requests.get(f"https://api.llama.fi/protocol/{Protocol}")

    # Check for status code
    if response.status_code != 200:
        raise Exception(f"Error: Received status code {response.status_code}")

    # Parse JSON data from response
    data = response.json()

    # Get list of chains
    chains = list(data["chainTvls"].keys())

    # Initialize empty list to store rows of data
    rows = []

    # Loop through each date in tvl_data
    for tvl in data["chainTvls"][chains[0]]["tvl"]:
        # Get date and totalLiquidityUSD
        date = tvl["date"]
        date_string = datetime.fromtimestamp(date).strftime("%Y-%m-%d %H:%M:%S")
        # Create dictionary with date
        row = {
            "date": date_string
        }
        # Add dictionary with tvl to row
        for chain in chains:
            # loop through the tvl of the current chain
            for chain_tvl in data["chainTvls"][chain]["tvl"]:
                # check if date matches
                if chain_tvl["date"] == date:
                    # if date matches, add totalLiquidityUSD
                    row[chain] = chain_tvl["totalLiquidityUSD"]
                    break
        # Add dictionary to rows list
        rows.append(row)

    # Write rows to CSV file
    with open("protocol_tvl_data.csv", "w") as csvfile:
        fieldnames = ["date"] + chains
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print("TVL data written to protoco_tvl_data.csv")

except Exception as e:
    print(f"Error: {e}")