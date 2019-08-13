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

        description = ' '
        addres = ''
        for i in item['description']:
            description += i
        for i in item['addres']:
            addres += i

        self.connection.rollback()
        self.cursor.execute("""INSERT INTO domria (price,uniqueID,number_of_rooms, floor, storeys,
                                                   total_space,living_space, kitchen_space, who_saler,
                                                   distance_center, type_center,type_heating,
                                                   distance_subway, type_subway, distance_market,
                                                   type_market,url,data_of_pulication, description, addres) 
                                        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""", 
        
        (item['price'][0],item['uniqueID'][0],item['number_of_rooms'][0],item['floor'][0],
         item['storeys'][0], item['total_space'][0], item['living_space'][0],
         item['kitchen_space'][0], item['who_saler'][0], item['distance_center'][0],
         item['type_center'][0], item['type_heating'][0], item['distance_subway'][0],
         item['type_subway'][0], item['distance_market'][0], item['type_market'][0],
         item['url'][0], item['data_of_pulication'][0], description,addres
        ))

        self.connection.commit()

        
        return item
