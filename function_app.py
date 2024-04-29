import azure.functions as func
import logging
from requests import Session
import json

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)
# Function to retrieve cryptocurrency prices
@app.route(route="http_trigger")
def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # API url and api key
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    api = '3388b957-7571-4ccd-8c6d-d1ade4e83c26'
    parameters = {
        'slug': 'bitcoin,xrp,dogecoin,bitcoin-cash,chainlink,solana,bnb,ethereum,cardano,hedera',
        'convert': 'USD'
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': api
    }

    session = Session()
    session.headers.update(headers)
    # Send request to CoinMarketCap API
    response = session.get(url, params=parameters)
    # Load JSON data
    data = json.loads(response.text)
    
    # Prepare JSON response
    result = {}
    # Extracting cryptocurrency prices by going over the data response
    for crypto in data['data'].values():
        # Extracting cryptocurrency price
        crypto_price = crypto['quote']['USD']['price']
        # Adding cryptocurrency price to the result
        result[crypto['slug'] + "_price"] = crypto_price
    # Return JSON response in organized format
    # Mimetype displays the response in JSON format
    if result:
        return func.HttpResponse(json.dumps(result), mimetype="application/json")
    else:
        # Case for failure
        return func.HttpResponse(
            "Failed to retrieve cryptocurrency prices.",
            status_code=500
        )