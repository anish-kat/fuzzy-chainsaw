import os
import json
import time
import logging
from kafka import KafkaProducer

# 1. Setup Logging (Industry Standard for SRE)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 2. Configuration from Environment (Security Best Practice)
KAFKA_BROKER = os.getenv("KAFKA_BROKER", "localhost:9092")
TOPIC = "scaling-signals"

def get_kafka_producer():
    """Connect to Kafka with retry logic."""
    for i in range(5):
        try:
            return KafkaProducer(
                bootstrap_servers=[KAFKA_BROKER],
                value_serializer=lambda v: json.dumps(v).encode('utf-8')
            )
        except Exception as e:
            logger.error(f"Kafka connection failed. Retry {i+1}/5...")
            time.sleep(5)
    raise Exception("Could not connect to Kafka.")

def predict_load():
    """
    Simulated ML logic. In production, this would call a model 
    or a Weather API to forecast a traffic spike.
    """
    # Simulate finding a 'Severe Weather' event
    is_storm_coming = True 
    
    if is_storm_coming:
        return {
            "version": "1.0",
            "timestamp": int(time.time()),
            "action": "scale_up",
            "target_replicas": 15,
            "metadata": {"reason": "Predicted Storm Spike", "confidence": 0.92}
        }
    return {"action": "maintain", "target_replicas": 2}

if __name__ == "__main__":
    logger.info("Atmosphere Predictor Engine Starting...")
    producer = get_kafka_producer()
    
    try:
        while True:
            signal = predict_load()
            producer.send(TOPIC, signal)
            logger.info(f"Published Signal: {signal['action']} -> {signal['target_replicas']} replicas")
            time.sleep(30) # Check every 30 seconds
    except KeyboardInterrupt:
        logger.info("Shutting down Predictor...")
