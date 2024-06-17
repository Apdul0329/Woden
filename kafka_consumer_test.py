from confluent_kafka import Consumer, KafkaError

# Kafka 컨슈머 설정
conf = {
    'bootstrap.servers': 'localhost:29092',
    'group.id': 'test-group',
    'auto.offset.reset': 'earliest'
}

# 컨슈머 인스턴스 생성
consumer = Consumer(conf)

# 토픽 구독
topics = ['StorageCreated']
consumer.subscribe(topics)

# 이벤트 수신 및 출력
try:
    while True:
        msg = consumer.poll(timeout=1.0)
        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                # 파티션 끝에 도달
                continue
            else:
                print(msg.error())
                break
        print('Received message: {}'.format(msg.value().decode('utf-8')))

except KeyboardInterrupt:
    pass

finally:
    consumer.close()
