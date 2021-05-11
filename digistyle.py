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
        box = soup.findAll("div", {"class":"cp-card cp-card--product-card"})
        for l in box:
            try:
                link = 'https://www.digistyle.com' + l.find('a', href=True)['href']
                img = l.find ('img')['src']
                name = l.find('div', {'class':'cp-card__footer'}).find('a').getText().replace('\n','').replace('  ','')
                price = l.find('div', {'class':'c-product-card__selling-price c-product-card__currency'}).getText().replace('\n','').replace('  ','')
                # sizes = [(s.find('a').getText()).replace(' ','').replace('\n','') for s in l.find('ul', {'class':'product-card-size'}).findAll('li')]
                brand = l.find('div', {'class':'c-product-card__brand'}).getText()
                
            except:
                link = ''
                img = ''
                name = ''
                price = ''
                # sizes = []
                brand = ''
                
            try:
                tak_size = l.find('div',{'class':'c-product-card__badge'}).getText()
            except:
                tak_size = ''
           
            try:
                 discount = l.find('div', {'class':'c-product-card__discount'}).getText().replace('\n','').replace('  ','')
                 last_price = l.find('del', {'class':'c-product-card__rrp-price'}).getText().replace('\n','').replace('  ','')
            except:
                 discount = ''
                 last_price = ''
           
            products.append({'link':link, 'img':img, 'brand': brand, 'name': name, 'tak_size':tak_size,
                             'price':price, 'last_price':last_price, 'discount':discount})
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


def all_digistyle(total_pages,subject):
    urls = ['https://www.digistyle.com/search/?q='+subject+'&pageno='+str(i) for i in range(1,int(total_pages)+1)]
    products = asyncio.run(run_all(urls))
    
    print(len(products))
    return(products) 


def special_digistyle(total_pages):
    urls = []
    for i in range(1,int(total_pages)+1):
        urls.append('https://www.digistyle.com/sales/mens-apparel/?pageno=' + str(i))
        urls.append('https://www.digistyle.com/sales/womens-apparel/?pageno=' + str(i))
        urls.append('https://www.digistyle.com/sales/personal-appliance/?pageno=' + str(i))
    products = asyncio.run(run_all(urls))
    
    print(len(products))
    return(products) 