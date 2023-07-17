# views.py
from django.shortcuts import render
from .models import Ad
import asyncio
import aiohttp
import json
import psycopg2


async def fetch(session, url, headers):
    async with session.get(url, headers=headers) as response:
        return await response.json()


async def parse_and_save_ads():
    conn = psycopg2.connect(
        host='localhost',
        database='news_2_parsing',
        user='postgres',
        password='6870'
)

    urls = [
        'https://lalafo.kg/api/search/v3/feed/search?expand=url&per-page=40&category_id=5830',
        'https://lalafo.kg/api/search/v3/feed/search?expand=url&per-page=40&category_id=2043',
        'https://lalafo.kg/api/search/v3/feed/search?expand=url&per-page=40&category_id=2046',
    ]

    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "device": "pc"
    }

    ads = []
    i = 0

    async with aiohttp.ClientSession() as session:
        for url in urls:
            data = await fetch(session, url, headers)
            items = data['items'][:1000]

            for item in items:
                i += 1
                if 21 > i > 0:
                    category = 1
                elif 41 > i > 20:
                    category = 2
                else:
                    category = 3

                images_list = [j['original_url'] for j in item['images']]
                images = ', '.join(images_list)

                ad = {
                    'title': item['title'],
                    'description': item['description'].replace('\n', ' '),
                    'price': item['price'],
                    'city': item['city'],
                    'images': images,
                    "phone": item['phone'],
                    "author": item['author'],
                    "category": category
                }
                ads.append(ad)

                title = ad['title']
                description = ad['description']
                price = ad['price']
                city = ad['city']
                phone = ad['phone']
                author = ad['author']
                category = ad['category']
                images = ad['images']

                # Insert the parsed data into the database
                with conn.cursor() as cursor:
                    cursor.execute(
                        """
                        INSERT INTO ads (title, description, price, city, phone, username, category, images)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                        """,
                        (title, description, price, city, phone, author, category, images)
                    )

    conn.commit()
    conn.close()


def create_ad(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        price = request.POST.get('price')
        city = request.POST.get('city')
        category = request.POST.get('category')
        photos = request.FILES.getlist('photos')
        phone = request.POST.get('phone')
        author = request.POST.get('author')

        ad = Ad(
            title=title,
            description=description,
            price=price,
            city=city,
            category=category,
            phone=phone,
            author=author
        )
        ad.save()

        for photo in photos:
            ad.photos.append(photo)
        ad.save()

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(parse_and_save_ads())

    return render(request, 'create_ad.html')
