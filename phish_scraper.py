import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
from datetime import datetime

class PhishScraper:
    def __init__(self):
        self.base_url = "https://raw.githubusercontent.com/openphish/public_feed/refs/heads/main/feed.txt"
        self.data = []

    def fetch_phishing_data(self):
        try:
            # يمكنك الحصول على API key من موقع PhishTank
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(self.base_url, headers=headers)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error: Status code {response.status_code}")
                return None
        except Exception as e:
            print(f"Error fetching data: {str(e)}")
            return None

    def process_data(self, raw_data):
        if not raw_data:
            return
        
        for entry in raw_data:
            phish_data = {
                'url': entry.get('url', ''),
                'phish_type': entry.get('phish_detail_url', ''),
                'submission_time': entry.get('submission_time', ''),
                'verified': entry.get('verified', ''),
                'target': entry.get('target', '')
            }
            self.data.append(phish_data)

    def save_to_csv(self, filename='phishing_data.csv'):
        if self.data:
            df = pd.DataFrame(self.data)
            df.to_csv(filename, index=False)
            print(f"Data saved to {filename}")
        else:
            print("No data to save")

    def run(self):
        print("Starting phishing data collection...")
        raw_data = self.fetch_phishing_data()
        if raw_data:
            self.process_data(raw_data)
            self.save_to_csv()
            print(f"Collected {len(self.data)} phishing entries")
        else:
            print("Failed to collect data")

if __name__ == "__main__":
    scraper = PhishScraper()
    scraper.run()
