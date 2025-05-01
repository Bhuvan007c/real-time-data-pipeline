import json
import time
import random
from datetime import datetime
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

event_types = ['click', 'view', 'purchase']

while True:
    message = {
        'user_id': random.randint(1, 100),
        'event_type': random.choice(event_types),
        'timestamp': datetime.utcnow().isoformat()
    }
    producer.send('user-events', value=message)
    print(f"Sent: {message}")
    time.sleep(1)
