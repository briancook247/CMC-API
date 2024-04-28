import azure.functions as func
import logging
from requests import Session
import json

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="http_trigger")
def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # API details
    url = 'http://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    api = '3388b957-7571-4ccd-8c6d-d1ade4e83c26'  # Be sure to secure your API keys appropriately in production
    parameters = {
        'slug': 'bitcoin',
        'convert': 'USD'
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': api
    }

    session = Session()
    session.headers.update(headers)
    response = session.get(url, params=parameters)
    data = json.loads(response.text)
    
    # Extracting Bitcoin price
    bitcoin_price = data['data']['1']['quote']['USD']['price']

    # Prepare JSON response
    if bitcoin_price:
        result = json.dumps({"bitcoin_price": bitcoin_price})
        return func.HttpResponse(result, mimetype="application/json")
    else:
        return func.HttpResponse(
            "Failed to retrieve Bitcoin price.",
            status_code=500
        )
