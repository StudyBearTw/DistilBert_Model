import requests
from bs4 import BeautifulSoup

url = "https://news.ycombinator.com/"
headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")
    titles = soup.find_all("a", class_="titlelink")
    for i, title in enumerate(titles[:5], 1):
        print(f"{i}. {title.get_text()} ({title['href']})")
else:
    print(f"Failed to fetch the page: {response.status_code}")

import pandas as pd

data = {"Title": ["Title 1", "Title 2"], "URL": ["https://url1.com", "https://url2.com"]}
df = pd.DataFrame(data)
df.to_csv("output.csv", index=False)