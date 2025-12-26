import os
import json
import time
import pandas as pd
import kagglehub
from kafka import KafkaProducer
from openai import OpenAI

# --- CONFIGURATION ---
KAFKA_BROKER = os.getenv('KAFKA_BROKER', 'atmosphere-bus-kafka.default.svc.cluster.local:9092')
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

producer = KafkaProducer(
    bootstrap_servers=[KAFKA_BROKER],
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

def analyze_with_llm(row):
    """Uses GPT-4o-mini to decide if we need to scale the infra."""
    prompt = f"""
    Analyze the following weather data and decide if it represents an extreme event 
    that would cause a surge in app traffic (heatwaves, storms, extreme wind).
    
    Data: {row.to_json()}
    
    Respond ONLY in JSON format:
    {{"action": "SCALE_UP" or "STABLE", "reason": "brief explanation"}}
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            response_format={ "type": "json_object" }
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        print(f"LLM Error: {e}")
        return {"action": "STABLE"}

def start_streaming():
    csv_path = get_dataset()
    df = pd.read_csv(csv_path)
    print(f"✅ Dataset loaded! Analyzing {len(df)} global locations...")

    for index, row in df.iterrows():
        # This heartbeat ensures the logs stay 'alive'
        city = row.get('location_name', 'Unknown')
        print(f"🕒 [{index}] Consulting AI for {city}...", flush=True)

        analysis = analyze_with_llm(row)
        
        if analysis["action"] == "SCALE_UP":
            print(f"🚨 AI ALERT for {city}: {analysis['reason']}", flush=True)
            producer.send('scaling-signals', value=analysis)
            producer.flush()
        
        time.sleep(2)

if __name__ == "__main__":
    start_streaming()
