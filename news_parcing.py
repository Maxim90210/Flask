import requests
from bs4 import BeautifulSoup

url = "https://scipost.org/atom/publications/comp-ai"

response = requests.get(url)

if response.status_code == 200:
    html_content = response.content

    soup = BeautifulSoup(html_content, 'html.parser')

    news_items = soup.find_all('entry') 
    parsed_news = []

    for item in news_items:
        title = item.find('title').text if item.find('title') else 'No Title'

        link = item.find('link')['href'] if item.find('link') else 'No Link'

        summary = item.find('summary').text if item.find('summary') else 'No Summary'

        parsed_news.append({
            'title': title,
            'link': link,
            'summary': summary
        })

    for news in parsed_news:
        print(f"Заголовок: {news['title']}")
        print(f"Посилання: {news['link']}")
        print(f"Текст: {news['summary']}\n")

else:
    print(f"Не вдалося отримати сторінку, статус код: {response.status_code}")
