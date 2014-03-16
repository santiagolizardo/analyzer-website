
from google.appengine.api import app_identity
from google.appengine.api import urlfetch

def createShortUrl( long_url ):
    scope = "https://www.googleapis.com/auth/urlshortener"
    authorization_token, _ = app_identity.get_access_token(scope)
    logging.info("Using token %s to represent identity %s",
                 authorization_token, app_identity.get_service_account_name())
    payload = json.dumps({"longUrl": long_url})
    response = urlfetch.fetch(
            "https://www.googleapis.com/urlshortener/v1/url?pp=1",
            method=urlfetch.POST,
            payload=payload,
            headers = {"Content-Type": "application/json",
                       "Authorization": "OAuth " + authorization_token})
    if response.status_code == 200:
        result = json.loads(response.content)
        return result["id"]
    raise Exception("Call failed. Status code %s. Body %s",
                    response.status_code, response.content)

