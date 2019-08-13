from __future__ import absolute_import
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from DomRiaParser.items import DomRiaItem
from scrapy.selector import Selector
import re

class DomRiaSpider(CrawlSpider):
    name = "DomRia"
    allowed_domains = ["dom.ria.com"]
    start_urls = ["https://dom.ria.com/prodazha-kvartir/kiev/?page=1"]

    rules = (
              Rule(LinkExtractor(allow=('page='), restrict_css=('a.page-link',)), follow=True),
              Rule(LinkExtractor(allow=('.html'),
                                 deny=['https://dom.ria.com/realty_add_new.html',
                                       'https://dom.ria.com/realty_search.html']),
                                 callback="parse_item",follow=False),
            )   
    
    def parse_item(self, response):
        
        l = ItemLoader(DomRiaItem(),response)

        floor = getIntObj(response,
                       '//*[@id="description"]/div[1]/div[3]/ul/li[2]/div[2]/text()')

        number_of_rooms = getIntObj(response,
                                '//*[@id="description"]/div[1]/div[3]/ul/li[1]/div[2]/text()')

        total_space, living_space, kitchen_space = getSpace(response,
                                '//*[@id="description"]/div[1]/div[3]/ul/li[4]/div[2]/text()')
       
        price = getObj(response,
                        '//*[@id="app"]/div[3]/div/div[3]/aside/ul[1]/li[1]/ul/li[1]/div/span[1]/text()')
        
        saler = getText(response,'//*[@id="description"]/div[1]/div[3]/ul/li[5]/div[2]/text()')

        addres = getText(response,'//*[@id="app"]/div[3]/div/div[2]/h1/text()')

        uniqueIDstr = getText(response,'//*[@id="app"]/div[3]/div/div[3]/aside/ul[4]/li[2]/b/text()')

        if uniqueIDstr:
            uniqueID = int(uniqueIDstr)
        else:
            uniqueID = None
        data_of_pulication = getText(response,'//*[@id="app"]/div[3]/div/div[3]/aside/ul[4]/li[1]/b/text()')

        storeys = getIntObj(response,'//*[@id="description"]/div[1]/div[3]/ul/li[3]/div[2]/text()')

        description = getDescript(response,'//*[@id="descriptionBlock"]/text()')

        center_dist, center_type, type_heating, subway_dist, subway_type, market_dist,market_type = getSubway(response,'//*[@id="additionalInfo"]//text()')
        
        #phone = getText(response,'//*[@id="app"]/div[3]/div/div[3]/aside/ul[2]/li[7]/div/span[1]//text()')
        print('\n\n\n', addres[0], '\n\n')

        

        
        l.add_value('description', description)
        l.add_value('storeys', storeys)       
        l.add_value('data_of_pulication',data_of_pulication)
        l.add_value('uniqueID',uniqueID)
        l.add_value('addres',str(addres))
        l.add_value('price', price)
        l.add_value('floor',floor)
        l.add_value('number_of_rooms',number_of_rooms)
        l.add_value('total_space',total_space)
        l.add_value('living_space',living_space)
        l.add_value('kitchen_space',kitchen_space)
        l.add_value('who_saler',saler)
        l.add_value('distance_center', center_dist)
        l.add_value('type_center', center_type)
        l.add_value('type_heating',type_heating)
        l.add_value('distance_subway',subway_dist)
        l.add_value('type_subway', subway_type)
        l.add_value('distance_market',market_dist)
        l.add_value('type_market',market_type)
        l.add_value('url', response.url)

        return l.load_item()

def getDescript(response,xpaz):
    selector = response.xpath(xpaz)
    string = ''
    for select in selector.xpath(xpaz):
        string += select.get('data=')
    string = selector.getall()
    return string

def getText(response,xpaz):
    """THis function for reading any text"""
    selector = Selector(response=response).xpath(xpaz).get()
    if type(selector) == str:
        selector = selector.strip()
    else: 
        selector = None
    return selector

def getObj(response,xpaz):
    """This function for reading price"""
    selector = Selector(response=response).xpath(xpaz).get()
    if type(selector) == str:
        selector = selector.strip()
    else: 
        return None
    price =''
    for char in selector:
        if char != ' ' and char != '$':
            price += char
    price = int(price)
    return price

def getIntObj(response,xpaz):
    """This funcrion for reading floor and amount of rooms"""
    selector = Selector(response=response).xpath(xpaz).get()
    if type(selector) == str:
        selector = selector.strip()
    else: 
        return None
    selector = float(selector[:3].strip())
    return selector
        
def getSpace(response,xpaz):
    """This function return size of apartamens """
    spaces = Selector(response=response).xpath(xpaz).get()
    if type(spaces) == str:
        spaces = spaces.strip()
    else: 
        return None
    total_split = [i for i in re.split(r'(\d+.\d+|\W+)', spaces) if i]
    
    total_space = None
    live_space = None
    kitchen_space = None
    
    sqear = [None]*3
    index = 0

    for string in total_split:
        if string.replace('.','',1).isdigit():
            sqear[index] = string
            index += 1

    if sqear[2] is None:
        if sqear[0]:
            total_space = float(sqear[0])
        else: 
            total_split = None
        if sqear[1]:
            kitchen_space = float(sqear[1])
        else: live_space = None
        
    else:
        total_space = float(sqear[0])
        live_space = float(sqear[1])
        kitchen_space = float(sqear[2])

    return total_space, live_space, kitchen_space
        
def getSubway(response, xpaz):

    selector = response.xpath(xpaz)
    listWithout = []
    lists = selector.getall()
    subway_dist,center_dist,center_type,type_heating,subway_type = None,None,None,None,None
    market_type,market_dist = None, None
    for element in lists:
        listWithout.append(element.strip())
    strings = ''
    for string in listWithout:
        strings += string
        strings += '  '
    total_split = [i for i in re.split(r'(до \d+-ти минут|\W+ )', strings) if i]
    flag_dist,flag_center,flag_space,flag_type,flag_point = False,False,False,False,False
    a,b,c,d = 0,0,0,0
    flag_heating,flag_subway,flag_distSub,flag_typeSubway = False,False,False,False
    flag_typeMarket,flag_distMarket,flag_market = False,False,False

    # it`s a realy bad code but i can`t creat something better maybe late
     
    for word in total_split:
        if word == 'до центра города':
            flag_center = True
        if word == '  ' and flag_center:
            flag_space = True
        if word == 'удаленность' and flag_space:
            continue
        if word == ': ' and flag_center:
            flag_dist = True
            continue
        if flag_dist:
            center_dist = word
            flag_center,flag_dist,flag_space = False,False,False
            flag_type = True
            continue
        if a < 3 and flag_type:
            a += 1
            continue
        if a == 3 and flag_type:
            flag_type = False
            center_type = word
            continue
        if word == 'отопление':
            flag_space = True
            b = 1
        if b < 3 and flag_space:
            b += 1
            flag_heating = True
            continue
        if b == 3 and flag_heating:
            flag_heating,flag_space = False, False
            type_heating = word
            continue
        if word == 'станция метро':
            flag_subway = True
        if word == ': ' and flag_subway:
            flag_distSub = True 
            continue
        if flag_distSub:
            subway_dist = word
            flag_subway,flag_distSub,flag_space = False,False,False
            flag_typeSubway = True
            continue
        if c < 3 and flag_typeSubway:
            c += 1
            continue
        if c == 3 and flag_typeSubway:
            flag_typeSubway = False
            subway_type = word
            continue
        if word == 'рынок':
            flag_market = True
        if word == ': ' and flag_market:
            flag_distMarket = True
            continue
        if flag_distMarket:
            market_dist = word
            flag_market,flag_distMarket,flag_space = False,False,False
            flag_typeMarket = True
            continue
        if c < 3 and flag_typeMarket:
            c += 1
            continue
        if c == 3 and flag_typeMarket:
            flag_typeMarket = False
            market_type = word
            continue
    return center_dist,center_type, type_heating, subway_dist,subway_type,market_dist,market_type

