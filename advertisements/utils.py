import requests
import json
from advertisements.models import Ad

def parse_and_save_ads():
    urls = [
        'https://lalafo.kg/api/search/v3/feed/search?expand=url&per-page=40&category_id=5830',
        'https://lalafo.kg/api/search/v3/feed/search?expand=url&per-page=40&category_id=2043',
        'https://lalafo.kg/api/search/v3/feed/search?expand=url&per-page=40&category_id=2046',
    ]

    all_ads = []

    for url in urls:
        ads = get_ads(url)
        all_ads.extend(ads)

    for ad_data in all_ads:
        ad = Ad(
            title=ad_data['title'],
            description=ad_data['description'],
            price=ad_data['price'],
            city=ad_data['city'],
            category=ad_data['category'],
            photos=ad_data['photos'],
            phone=ad_data['phone'],
            author=ad_data['author']
        )
        ad.save()

def get_ads(url):
    response = requests.get(url)
    data = response.json()
    return data['data']
