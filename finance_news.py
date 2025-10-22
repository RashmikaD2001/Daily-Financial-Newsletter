from dotenv import load_dotenv
import os
import yfinance as yf
import requests
import json

load_dotenv()

API_KEY = os.getenv("NEWS_API_KEY")
if not API_KEY:
    raise ValueError("NEWS_API_KEY environment variable is required")

# Fixed API endpoint
API_ENDPOINT = f"https://financialmodelingprep.com/stable/fmp-articles?page=0&limit=20&apikey={API_KEY}"

def getNews():
    try:
        # Changed from POST to GET
        response = requests.get(API_ENDPOINT)
        response.raise_for_status()
        
        # Fixed JSON parsing - use .json() method
        articles = response.json()
        
        # Remove "image" and "id" from each article
        cleaned_articles = []
        for article in articles:
            cleaned_article = {k: v for k, v in article.items() if k not in ["image", "id"]}
            cleaned_articles.append(cleaned_article)
        
        return cleaned_articles
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching news: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON response: {e}")
        return None

def getData(cleaned_articles):
    # Add null check
    if cleaned_articles is None:
        print("No articles to process")
        return {}
    
    financial_data = {}
    
    for article in cleaned_articles:
        tickers_field = article.get("tickers")  # e.g. "NYSE:MRK"
        
        if not tickers_field:
            continue
        
        # Extract the raw ticker symbol (remove prefix like "NYSE:")
        ticker_symbol = tickers_field.split(":")[-1]
        
        try:
            ticker = yf.Ticker(ticker_symbol)
            
            financial_data[ticker_symbol] = {
                "article": {
                    "title": article.get("title"),
                    "date": article.get("date"),
                    "content": article.get("content"),
                    "link": article.get("link"),
                    "author": article.get("author"),
                    "site": article.get("site")
                },
                "info": ticker.info,
                "history": ticker.history(period="1d").to_dict()
            }
        except Exception as e:
            print(f"Error fetching data for {ticker_symbol}: {e}")
            continue
    
    return financial_data