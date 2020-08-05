# Example code adapted from Requests-OAuthlib documentation
# https://requests-oauthlib.readthedocs.io/en/latest/examples/real_world_example.html
# Dependencies: pip install flask requests_oauthlib

from requests_oauthlib import OAuth2Session
from flask import Flask, request, redirect, session, url_for
from flask.json import jsonify
import os

app = Flask(__name__)

authorization_base_url = 'https://freesound.org/apiv2/oauth2/authorize/'
token_url = 'https://freesound.org/apiv2/oauth2/access_token/'

# The information below is obtained upon registration of new Freesound API
# credentials here: http://freesound.org/apiv2/apply
# See documentation of "Step 3" below to understand how to fill in the 
# "Callback URL" field when registering the new credentials.

with open("_FV_freesound_client_id.txt", "r") as id_file:
    client_id = id_file.read()

with open("_FV_freesound_API_key.txt", "r") as key_file:
    client_secret = key_file.read()


@app.route("/")
def demo():
    """Step 1: User Authorization.

    Redirect the user/resource owner to the OAuth provider (i.e. Freesound)
    using an URL with a few key OAuth parameters.
    """
    freesound = OAuth2Session(client_id)
    authorization_url, state = freesound.authorization_url(authorization_base_url)

    # State is used to prevent CSRF, keep this for later.
    session['oauth_state'] = state
    return redirect(authorization_url)
    

# Step 2: User authorization, this happens on the provider.

@app.route("/callback", methods=["GET"])
def callback():
    """ Step 3: Retrieving an access token.

    The user has been redirected back from the provider to your registered
    callback URL. With this redirection comes an authorization code included
    in the redirect URL. We will use that to obtain an access token.

    Note that the URL at which your app is serving this view is the 
    "Callback URL" that you have to put in the API credentials you create
    at Freesound. If running this code example unchanged, the callback URL 
    should be: http://localhost:5000/callback
    """

    freesound = OAuth2Session(client_id, state=session['oauth_state'])
    token = freesound.fetch_token(token_url, client_secret=client_secret, 
                                  authorization_response=request.url)
    print(token)
    # If you're using the freesound-python client library to access
    # Freesound, this is the token you should use to make OAuth2 requests
    # You should set the token like: 
    #     client.set_token(token,"oauth2")
    
    # However, for this example lets lets save the token and show how to
    # access a protected resource that will return some info about the user account 
    # who has just been authenticated using OAuth2. We redirect to the /profile
    # route of this app which will query Freesound for the user account details.
    session['oauth_token'] = token

    return redirect(url_for('.profile'))


@app.route("/profile", methods=["GET"])
def profile():
    """Fetching a protected resource using an OAuth 2 token.
    """
    freesound = OAuth2Session(client_id, token=session['oauth_token'])
    return jsonify(freesound.get('https://freesound.org/apiv2/me').json())


if __name__ == "__main__":
    # This allows us to use a plain HTTP callback
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = "1"
    app.secret_key = os.urandom(24)
    app.run(debug=True)