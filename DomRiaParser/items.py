# -*- coding: utf-8 -*-

from scrapy import Item, Field

class DomRiaItem(Item):
    number_of_rooms     = Field()
    total_space         = Field()
    price               = Field()
    living_space        = Field()
    kitchen_space       = Field()
    who_saler           = Field()
    floor               = Field()
    storeys             = Field() #count of all floors
    distance_center     = Field()
    type_center         = Field()
    type_heating        = Field()
    distance_subway     = Field()
    type_subway         = Field()
    distance_market     = Field()
    type_market         = Field()

    picture             = Field()
    
    url                 = Field()
    addres              = Field()
    uniqueID            = Field()
    data_of_pulication  = Field()
    description         = Field()