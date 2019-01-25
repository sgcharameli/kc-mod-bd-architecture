# -*- coding: utf-8 -*-

import requests
import time
from random import randint
from kafka import KafkaProducer

KAFKA_URI="10.142.0.3:9092"
KAFKA_DATA_PRODUCER_TOPIC="testkafka"

# Lista de códigos postales de madrid https://www.codigospostales.com/nestcp.cgi?28
# https://www.fotocasa.es/es/robots.txt

madrid_cp_list = [28001, 28002, 28003, 28004, 28005, 28006, 28007, 28008, 28009, 28010, 28011, 28012, 28013, 28014, 28015, 28016, 28017, 28018, 28019, 28020, 28021, 28022, 28023, 28024, 28025, 28026, 28027, 28028, 28029, 28030, 28031, 28032, 28033, 28034, 28035, 28036, 28037, 28038, 28039, 28040, 28041, 28042, 28043, 28044, 28045, 28046, 28047, 28048, 28049, 28050, 28051, 28052, 28053, 28054, 28055]

# short_cp_list = [28033, 28055, 28933, 28806]
short_cp_list = [28933]

print(short_cp_list)

producer = KafkaProducer(bootstrap_servers=KAFKA_URI)

for current_cp in short_cp_list:
  
  real_estates_num = 0;
  pageNum = 1;
  
  print("Obteniendo inmuebles del Código Postal: " + str(current_cp))
  
  while True:
    
    response = requests.get("https://api.fotocasa.es/PropertySearch/Search?combinedLocationIds=724,0,0,0,0,0,0,0,0&culture=es-ES&hrefLangCultures=ca-ES%3Bes-ES%3Bde-DE%3Ben-GB&isNewConstruction=false&isMap=false&latitude=40&longitude=-4&pageNumber=" + str(pageNum) + "&platformId=1&propertyTypeId=2&sortOrderDesc=true&sortType=bumpdate&text=" + str(current_cp) + "&transactionTypeId=1", headers={'user-agent': 'rogerbot'})

    result_json = response.json()

    real_estates = result_json['realEstates']
  
    real_estates_total = result_json['count']
  
    real_estates_num = real_estates_num + len(real_estates)
    
    #
    # send to kafka/rabbit
    #
    # producer.send(KAFKA_DATA_PRODUCER_TOPIC, str.encode(result_json), key=sensor.encode())
    producer.send(KAFKA_DATA_PRODUCER_TOPIC, str.encode(result_json))
    # print(json.dumps(result, indent=4))
    #
    
    print("\tObtenidos " + str(real_estates_num) + " inmuebles de " + str(real_estates_total) + " para el CP: " + str(current_cp))
    
    pageNum += 1
    
    # Por no ser muy pesaos pidiendo datos
    time.sleep(randint(3, 9))
    
    if ( real_estates_num >= real_estates_total ):
      break
    
  print("Obteniendo inmuebles en el Código Postal: " + str(current_cp) + " cargados " + str(real_estates_num) + " inmuebles de " + str(real_estates_total))
  
        
  

