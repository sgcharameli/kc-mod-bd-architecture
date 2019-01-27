# kc-mod-bd-architecture

Práctica del módulo big data architecture del Bootcamp III Edición Big Data &amp; Machine Learning

## Sprint 1

### Arquitectura

Se desea conocer la evolución de precios de viviendas e inmuebles de la comunidad de madrid. Para ello se ha desarrollado un script para consultar de forma diaria las viviendas consultando un api público. Para ello:
- Este api se ha descubierto analizando las peticiones de red del navegador mientras se navegaba por la web en cuestión.
- Como resultado de este análisis, se ha podido ver que las respuestas del servidor venían paginadas en tamaño de 30. Por tanto, se ha desarrollado el script contemplando esta situación para traernos todos los inmuebles de forma paginada.
- Además, se ha implementado un pequeño mecanismo de espera aleatorio (entre 3 y 9 segundos) entre peticiones para no sobrecargar el servidor ni generar posibles "alarmas".
- Este script está programado para ejecutarse todos los días mediante un crontab desde un servidor dedicado en GCP.
- Cada respuesta es enviada a una cola de mensajería, en este caso kafka, alojado en GCP, que se encargará de retener el mensaje hasta su entrega de forma asíncrona.
- Se ha tenido que configurar en kafka la siguiente línea en el server.properties:
'''
advertised.listeners=PLAINTEXT://[instance_public_id_address]:9092
'''
- Kafka estará conectado con un cluster de hadoop a través de flume. La idea de flume es desacoplar el destinatario de la fuente, de forma que si cambiase, sólo haya que retocar la configuración del sink de flume.
- Configuración de flume:

'''
flume1.sources  = kafka-source-1
flume1.channels = hdfs-channel-1
flume1.sinks    = hdfs-sink-1

flume1.sources.kafka-source-1.type = org.apache.flume.source.kafka.KafkaSource
flume1.sources.kafka-source-1.zookeeperConnect = XXX.XXX.XXX.XXX:2181
flume1.sources.kafka-source-1.topic =testkafka
flume1.sources.kafka-source-1.batchSize = 100
flume1.sources.kafka-source-1.channels = hdfs-channel-1

flume1.channels.hdfs-channel-1.type   = memory
flume1.sinks.hdfs-sink-1.channel = hdfs-channel-1
flume1.sinks.hdfs-sink-1.type = hdfs
flume1.sinks.hdfs-sink-1.hdfs.writeFormat = Text
flume1.sinks.hdfs-sink-1.hdfs.fileType = DataStream
flume1.sinks.hdfs-sink-1.hdfs.filePrefix = test-events
flume1.sinks.hdfs-sink-1.hdfs.useLocalTimeStamp = true
flume1.sinks.hdfs-sink-1.hdfs.path = /sink-from-kafka/%{topic}/%y-%m-%d
flume1.sinks.hdfs-sink-1.hdfs.rollCount=100
flume1.sinks.hdfs-sink-1.hdfs.rollSize=0
flume1.channels.hdfs-channel-1.capacity = 10000
flume1.channels.hdfs-channel-1.transactionCapacity = 1000
'''
- Para lanzar flume:
'''
flume-ng agent -n flume1 -c conf -f kafka-2-hadoop.conf - Dflume.root.logger=INFO,console
'''

- Se ha optado por configurar el cluster de hadoop fuera del GCP sencillamente por reaprovechar unas máquinas que habían quedado en desuso. Si esto no hubiese sido así, se hubiese montado un dataproc en GCP.
- Después del procesamiento de la información con hadoop, se insertará en un índice de elasticsearch la información generada para su posterior consulta en un cuadro de mando de kibana, ambos alojados en GCP.

- Diseño de la arquitectura:

https://docs.google.com/drawings/d/1yG7J_xdN8bGk-ZMIK81IF-bD6kr0E2Y4u4EnDAEWqrc/edit?usp=sharing


## Sprint 2

- El script se puede ver en google colab:

https://colab.research.google.com/drive/1-QvK3-ITZv-4ijFrEH0b45pdlBbZtVCJ

Se han comentado las líneas con la integración con kafka por no estar disponibles las librerías de kafka en el jupyter de google.


## Sprint 3

Se ha optado por montar un cluster hadoop con docker compose. Se adjuntan ficheros de configuración.
- Configurar en todas las instancias los ficheros core-site.xml y yarn-site.xml con el id del contenedor del master.
- Configurar únicamente en la instancia master los ids de los contenedores esclavos.

![alt text](https://raw.githubusercontent.com/username/projectname/branch/path/to/img.png)

# Arranque

Para iniciar los contenedores docker:
```
docker-compose up -d --build

docker-compose stop

docker-compose start
```


## Sprint 4


## Sprint 5
