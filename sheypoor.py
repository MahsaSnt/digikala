import asyncio
from arsenic import get_session, browsers, services
from bs4 import BeautifulSoup
import logging
import structlog


def set_arsenic_log_level(level = logging.WARNING):
    logger = logging.getLogger('arsenic')

    def logger_factory():
        return logger

    structlog.configure(logger_factory=logger_factory)
    logger.setLevel(level)

async def scraper_all(url):
    service = services.Chromedriver()
    browser = browsers.Chrome()
    browser.capabilities = {
        "goog:chromeOptions": {"args": ["--headless", "--disable-gpu"]}
    }
    async with get_session(service, browser) as session:
        await asyncio.wait_for(session.get(url),timeout=100)
        
        body = await session.get_page_source()
        soup = BeautifulSoup(body, 'html.parser')
        products = []
        box = soup.findAll("article", {"class":"serp-item list"})
        for l in box:
            try:
                link = l.find('a', href=True)['href']
                img = l.find ('img')['src']
                name = l.find('h2').find('a').getText()
                time = l.find('time').getText()
                price = l.find('strong',{'class': 'item-price'}).getText()
                
            except:
                link = ''
                img = ''
                name = ''
                price = ''
                time = ''
                
            try:
                region = l.find('div',{'class':'content'}).findAll('p')[1].getText()
            except:
                region = ''
           
           
            products.append({'link':link, 'img':img, 'name': name, 
                             'price':price, 'time':time, 'region':region})
        return products


async def run_all(urls):
    set_arsenic_log_level()
    result = []
    for url in urls:
        result.append(
            asyncio.create_task(scraper_all(url))
        )
    results = await asyncio.gather(*result)
    products = []
    for r in results:
        products = products + r  
    return products


def all_sheypoor(total_pages,subject, county):
    urls = ['https://www.sheypoor.com/' + county + '?q=' + subject + '&p=' + str(i) for i in range(1,int(total_pages)+1)]
    products = asyncio.run(run_all(urls))
    
    print(len(products))
    return(products) 


