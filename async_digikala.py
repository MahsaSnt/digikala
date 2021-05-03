import asyncio
from aiohttp import ClientSession
import nest_asyncio
import lxml.html
import pandas as pd
import time
import json

# nest_asyncio.apply()

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
    }
async def fetch(url, session, page):
    async with session.get(url) as response:
        html_body = await response.text()
        return {"body": html_body, "page": page}

async def fetch_with_sem(sem, session, url, page):
    async with sem:
        return await fetch(url, session, page)

async def main(total,subject):
    tasks = []
    sem = asyncio.Semaphore(10)
    async with ClientSession(headers=headers) as session:
        for i in range(1, int(total)+1):
            url = 'https://www.digikala.com/search/?has_selling_stock=1&q='+subject+'&pageno='+str(i)+'&sortby=21'
            #print("page", i, url)
            tasks.append(
                asyncio.create_task(
                    fetch_with_sem(sem, session, url, i)
                )
            )
        pages_content = await asyncio.gather(*tasks) 
        return pages_content


def output(total_pages,subject):
    results = asyncio.run(main(total_pages,subject))
    products=[]

    for result in results:
        html_data = result.get('body')
        tree=lxml.html.fromstring(html_data)
    
        for product in tree.xpath("//ul[@class='c-listing__items js-plp-products-list']/li"):
            name = product.xpath(".//div/@data-title-fa")[0]
            price= product.xpath(".//div/@data-price")[0]
            link = 'https://www.digikala.com'+product.xpath(".//a/@href")[0]
            pic = product.xpath(".//a/img/@src")[0]
            rate = product.xpath("normalize-space(//div[@class='c-product-box__engagement-rating']/text())")[0]
            products.append({'name':name, 'price':price, 'link':link, 'photo':pic, 'rate':rate})

    return(products)


