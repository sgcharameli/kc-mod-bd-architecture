# -*- coding: utf-8 -*-

import requests
import time
from random import randint
from kafka import KafkaProducer

KAFKA_URI="10.142.0.3:9092"
KAFKA_DATA_PRODUCER_TOPIC="testkafka"

# Lista de códigos postales de madrid http://www.madrid.org/iestadis/fijas/estructu/general/territorio/estructucartemcop.htm

# https://www.fotocasa.es/es/robots.txt

madrid_cp_list = [28000, 28001, 28002, 28003, 28004, 28005, 28006, 28007, 28008, 28009, 28010, 28011, 28012, 28013, 28014, 28015, 28016, 28017, 28018, 28019, 28020, 28021, 28022, 28023, 28024, 28025, 28026, 28027, 28028, 28029, 28030, 28031, 28032, 28033, 28034, 28035, 28036, 28037, 28038, 28039, 28040, 28041, 28042, 28043, 28044, 28045, 28046, 28047, 28048, 28049, 28050, 28051, 28052, 28053, 28054, 28055, 28100, 28100, 28108, 28109, 28110, 28119, 28120, 28130, 28140, 28150, 28160, 28170, 28180, 28189, 28190, 28191, 28192, 28193, 28194, 28195, 28196, 28200, 28200, 28209, 28210, 28211, 28212, 28213, 28214, 28219, 28220, 28221, 28222, 28223, 28224, 28229, 28231, 28232, 28240, 28248, 28250, 28260, 28270, 28280, 28290, 28292, 28293, 28294, 28295, 28296, 28297, 28300, 28300, 28310, 28311, 28312, 28320, 28330, 28341, 28342, 28343, 28350, 28359, 28360, 28370, 28380, 28390, 28391, 28400, 28400, 28410, 28411, 28412, 28413, 28420, 28430, 28440, 28450, 28459, 28460, 28470, 28479, 28480, 28490, 28491, 28492, 28500, 28500, 28510, 28511, 28512, 28513, 28514, 28515, 28521, 28522, 28523, 28524, 28529, 28530, 28540, 28550, 28560, 28570, 28580, 28590, 28594, 28595, 28596, 28597, 28598, 28600, 28600, 28607, 28609, 28610, 28620, 28630, 28640, 28648, 28649, 28650, 28660, 28670, 28679, 28680, 28690, 28691, 28692, 28693, 28694, 28695, 28696, 28700, 28701, 28702, 28703, 28706, 28707, 28708, 28709, 28710, 28720, 28721, 28722, 28723, 28729, 28730, 28737, 28739, 28740, 28741, 28742, 28743, 28749, 28750, 28751, 28752, 28753, 28754, 28755, 28756, 28760, 28770, 28780, 28790, 28791, 28792, 28793, 28794, 28800, 28801, 28802, 28803, 28804, 28805, 28806, 28807, 28810, 28811, 28812, 28813, 28814, 28815, 28816, 28817, 28818, 28821, 28822, 28823, 28830, 28840, 28850, 28860, 28861, 28862, 28863, 28864, 28880, 28890, 28891, 28900, 28901, 28902, 28903, 28904, 28905, 28906, 28907, 28909, 28911, 28912, 28913, 28914, 28915, 28916, 28917, 28918, 28919, 28921, 28922, 28923, 28924, 28925, 28931, 28932, 28933, 28934, 28935, 28936, 28937, 28938, 28939, 28940, 28941, 28942, 28943, 28944, 28945, 28946, 28947, 28950, 28970, 28971, 28976, 28977, 28978, 28979, 28981, 28982, 28983, 28984, 28990, 28991]

print(madrid_cp_list)

producer = KafkaProducer(bootstrap_servers=KAFKA_URI)

for current_cp in madrid_cp_list:
  
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
    producer.send(KAFKA_DATA_PRODUCER_TOPIC, str.encode(str(result_json)))
    # print(json.dumps(result, indent=4))
    #
    
    print("\tObtenidos " + str(real_estates_num) + " inmuebles de " + str(real_estates_total) + " para el CP: " + str(current_cp))
    
    pageNum += 1
    
    # Por no ser muy pesaos pidiendo datos
    time.sleep(randint(3, 9))
    
    if ( real_estates_num >= real_estates_total ):
      break
    
  print("Obteniendo inmuebles en el Código Postal: " + str(current_cp) + " cargados " + str(real_estates_num) + " inmuebles de " + str(real_estates_total))
