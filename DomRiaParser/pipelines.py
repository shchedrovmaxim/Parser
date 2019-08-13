# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


import psycopg2



def conectToBase(user:str, password:str, host:str, 
                 port:str, database:str):
    
    try:
        connection = psycopg2.connect(user = user, password = password,
                                      host = host, port = port, database = database)

    except (Exception, psycopg2.Error) as error :
        print ("Error while connecting to PostgreSQL", error)
    
    return connection

class DomriaparserPipeline(object):
    def open_spider(self, spider):
        host = '172.18.0.2'
        user = 'postgres'
        password = 'changeme' 
        database = 'postgres'
        port = '5432'
        self.connection = conectToBase(user=user, password=password, host=host,
                                       port=port, database=database)
        self.cursor = self.connection.cursor()

    def close_spider(self, spider):
        self.cursor.close()
        self.connection.close()

    def process_item(self, item, spider):
        # query = """INSERT INTO domria (number_of_rooms,
        # total_space, price, living_space,kitchen_space,
        # who_saler, floor, storeys, distance_center,
        # type_center, type_heating, distance_subway,
        # type_subway, distance_market, type_market, url,
        # addres, uniqueID, data_of_pulication, description)
        # VALUES(%d,%lf,%d,%lf,%lf,%s,%d,%d,%s,%s,%s,%s,%s,%s,%s,%s,%s,%d,%s,%s)
        #  """"INSERT INTO domria(price) VALUES(%s)" ,(item['price'])
        query = "INSERT INTO domria('addres') VALUES("
        
        self.cursor.execute("insert into domria(price) VALUES(%s)" ,(item['price']) )
      
        self.connection.autocommit(True)
        return item
