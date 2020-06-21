import json
import time
import requests
import pandas as pd

# Add your Bing Search V7 subscription key and endpoint to your environment variables.
subscription_key = "SUB_KEY"
endpoint = "ENDPOINT_KEY"

# Query term(s) to search for.
query = input("Enter query string: ")
amount = int(input("Enter amount (multiples of 50): ")) / 50

#File timestamp
t = time.localtime()
timestamp = time.strftime('%b-%d-%Y_%H%M%S', t)

counter = 0
finalDF = pd.DataFrame()
while counter < amount:
    # Construct a request
    mkt = 'en-US'
    params = { 'q': query, 'mkt': mkt , 'count': '50', 'offset': (counter * 50) + 1, 'responseFilter':'webpages'}
    headers = { 'Ocp-Apim-Subscription-Key': subscription_key }


    # Call the API
    try:
        response = requests.get(endpoint, headers=headers, params=params)
        response.raise_for_status()
        webpages = response.json()['webPages']
        webValues = webpages['value']
        pdFrame = pd.DataFrame(webValues)
        pdFrame.index += ((counter * 50 ) + 1)
        finalDF = finalDF.append(pdFrame)
    except Exception as ex:
        raise ex
    counter += 1

t = open(query.replace(" ", "_") + "_" + timestamp +".csv", "w")
t.write(finalDF.to_csv())
t.close()
