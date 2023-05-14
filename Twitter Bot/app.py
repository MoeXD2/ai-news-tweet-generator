import requests
import json
import os
import openai
from flask import Flask, render_template, jsonify, request, redirect, url_for, flash, session
from flask import current_app
from requests_oauthlib import OAuth1Session


app = Flask(__name__)
app.config['SECRET_KEY'] = "YOUR_SECRET_KEY"

# Bing Web Search API credentials
BING_API_KEY = "YOUR_BING_API_KEY"

# Twitter and OpenAI API credentials
OPENAI_API_KEY = 'YOUR_API_KEY'
consumer_key = 'YOUR_KEY'
consumer_secret = 'YOUR_KEY'
access_token = 'YOUR_TOKEN'
access_token_secret = 'YOUR_TOKEN'

# Set up OpenAI API
openai.api_key = OPENAI_API_KEY

def fetch_ai_llm_news():
   search_url = "https://api.bing.microsoft.com/v7.0/news/search"
   headers = {"Ocp-Apim-Subscription-Key": BING_API_KEY}
   params = {
      "q": "YOUR OWN SEARCH PARAMETERS",
      "count": 5,
      "mkt": "en-US"  # Set the market to English (United States) or Whatever you prefer
   }
   
   response = requests.get(search_url, headers = headers, params = params)
   return response.json()["value"]


def create_tweet_with_chatgpt(news_articles):
   news_items = "\n".join([f"{i+1}. {article['name']} - {article['description']} - {article['url']}" for i, article in enumerate(news_articles)])
   prompt = f"Here are the latest (YOUR CHOICE OF NEWS) news articles:\n{news_items}\n\nBased on these articles, write a short tweet (not more than 280 characters) about the most interesting one, and add the link to it at the end of the tweet."
   
   messages = [
      {"role": "system", "content": "You are a helpful assistant that writes tweets about (SAME HERE) news, make sure the tweet is not too long and is short (not more than 280 characters) and insightful, pick the most interesting tweet possible. Make sure to include the link to the article(s) you based the tweet on"},
      {"role": "user", "content": prompt}
   ]

   response = openai.ChatCompletion.create(
      model = "gpt-3.5-turbo",
      messages = messages,
      temperature = 0.8,
      max_tokens = 400,
      frequency_penalty = 0,
      presence_penalty = 0,
   )

   tweet = response['choices'][0]['message']['content'].strip()
   return tweet


def authenticate(api_key, api_key_secret, access_token, access_token_secret):
   return OAuth1Session(api_key, client_secret=api_key_secret, resource_owner_key=access_token, resource_owner_secret=access_token_secret)


def post_tweet_v2(tweet):
   # Authenticate with Twitter
   auth_session = authenticate(consumer_key, consumer_secret, access_token, access_token_secret)

   # Create a Tweet using Twitter API v2
   url = "https://api.twitter.com/2/tweets"
   payload = {"text": tweet}
   headers = {'Content-Type': 'application/json'}
   response = auth_session.post(url, data = json.dumps(payload), headers = headers)

   if response.status_code == 201:
      print("Tweet posted successfully!")
   else:
      print(f"An error occurred: {response.text}")



@app.route('/callback')
def callback():
   # Handle the OAuth callback and complete the authentication process
   pass


@app.route("/generate_tweet", methods = ["POST"])
def generate_tweet():
   news = fetch_ai_llm_news()
   tweet = create_tweet_with_chatgpt(news)
   return jsonify(news = news, tweet = tweet)
 

@app.route("/post_tweet", methods = ["POST"])
def post_tweet_route():
   tweet = request.form.get("tweet")
   try:
      post_tweet_v2(tweet)
      return jsonify(status = "success")
   except ValueError:
      return jsonify(status = "failed")


@app.route("/")
def home():
   if 'logged_in' not in session or not session['logged_in']:
      return redirect(url_for('login'))
   return render_template("index.html", current_app = current_app)

@app.route('/logout')
def logout():
   session.pop('logged_in', None)
   flash('You have been logged out', 'success')
   return redirect(url_for('login'))

@app.route("/login", methods=["GET", "POST"])
def login():
   if request.method == "POST":
      username = request.form["username"]
      password = request.form["password"]
      
      if username == "YOUR USER NAME" and password == "YOUR PASSWORD":
         session['logged_in'] = True
         # Redirect to the main page if login is successful
         return redirect(url_for('home'))
      else:
         # Show an error message if login fails
         flash("Invalid username or password", "danger")
         return redirect(url_for("login"))

   return render_template("login.html")


if __name__ == "__main__":
   app.run(debug = True)
