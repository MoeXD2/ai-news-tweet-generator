# AI News Tweet Generator

AI News Tweet Generator is a Flask web application that uses OpenAI's GPT-3.5-turbo to generate tweets about the latest news in artificial intelligence (AI) and large language models (LLMs). This application fetches the latest news articles from the Bing News API and then uses GPT-3.5-turbo to create an engaging tweet about the most interesting article among the fetched news.

## Features

- Fetches the latest AI and LLM news from the Bing News API
- Uses OpenAI's GPT-3.5-turbo to generate tweets based on the most interesting news article
- Provides a simple user interface to generate and review tweets
- Allows users to post the generated tweets to Twitter

## Installation and Setup

1. Clone the repository to your local machine:
```
git clone https://github.com/MoeXD2/ai-news-tweet-generator.git
```

2. Change to the project directory:
```
cd ai-news-tweet-generator
```

3. Install the required dependencies:
```
pip install -r requirements.txt
```

4. Create a `.env` file in the project directory and add your API keys:
```
OPENAI_API_KEY=<your_openai_api_key>
BING_API_KEY=<your_bing_api_key>
TWITTER_API_KEY=<your_twitter_api_key>
TWITTER_API_SECRET=<your_twitter_api_secret>
TWITTER_ACCESS_TOKEN=<your_twitter_access_token>
TWITTER_ACCESS_TOKEN_SECRET=<your_twitter_access_token_secret>
```

5. Run the Flask application:
```
flask run
```

6. Open your web browser and visit `http://127.0.0.1:5000/` to access the application.

## Usage

1. Log in with the provided username and password.
2. Click the "Generate Tweet" button to fetch the latest AI and LLM news and generate a tweet based on the most interesting article.
3. Review the generated tweet, and click the "Post Tweet" button to post it to your Twitter account.
4. Log out when you're finished.
