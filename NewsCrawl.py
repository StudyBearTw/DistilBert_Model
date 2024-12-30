import requests
from bs4 import BeautifulSoup
import csv
import concurrent.futures
import time

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

# 爬取單篇新聞
def fetch_yahoo_news(url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            title = soup.find('h1').get_text() if soup.find('h1') else '無標題'
            paragraphs = soup.find_all('p')
            content = "\n".join([p.get_text() for p in paragraphs])
            print(f"已爬取: {title}")
            return {
                'title': title,
                'content': content,
                'url': url
            }
        else:
            print(f"訪問失敗: {url}")
            return None
    except Exception as e:
        print(f"爬取錯誤: {url} - {str(e)}")
        return None

# 爬取新聞首頁的連結
def fetch_news_links(homepage_url):
    response = requests.get(homepage_url, headers=HEADERS)
    links = []
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        for a in soup.find_all('a', href=True):
            href = a['href']
            if '/news/' in href and href.startswith('https'):
                links.append(href)
    return list(set(links))

# 儲存爬取結果
def save_to_csv(news_list, filename='yahoo_news.csv'):
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['標題', '內容', '網址'])
        for news in news_list:
            writer.writerow([news['title'], news['content'], news['url']])

# 多線程爬取
def main():
    homepage = 'https://tw.news.yahoo.com/'
    news_links = fetch_news_links(homepage)
    
    all_news = []
    max_threads = 10  # 最大執行緒數量

    # 使用 ThreadPoolExecutor 進行多線程爬取
    with concurrent.futures.ThreadPoolExecutor(max_threads) as executor:
        futures = [executor.submit(fetch_yahoo_news, link) for link in news_links]
        
        for future in concurrent.futures.as_completed(futures):
            news = future.result()
            if news:
                all_news.append(news)

    # 儲存爬取結果到 CSV
    save_to_csv(all_news)
    print("新聞爬取完成，結果已儲存。")

if __name__ == '__main__':
    main()
