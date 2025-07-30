# Smartbike Telemetry MQTT Client
# This script subscribes to Smartbike telemetry and brake button topics
# using wildcard support for multiple bikes, and logs structured output.

import paho.mqtt.client as mqtt
import json
from mqtt_ingestor import process_payload  # Import custom payload processor

# MQTT Broker configuration
BROKER = "10.137.0.149"  # IP address of the Mosquitto broker
PORT = 1883              # Default MQTT port (non-TLS)

# MQTT topics to subscribe to (wildcard + supports all Smartbikes)
TOPICS = [
    "bike/+/speed/report",     # Speed telemetry
    "bike/+/power/report",     # Power telemetry
    "bike/+/cadence/report",   # Cadence telemetry
    "bike/+/button/report"     # Button input for the breaking
]

def on_connect(client, userdata, flags, rc):
    """
    Callback function triggered upon successful connection to the MQTT broker.
    Subscribes to all specified Smartbike topics.
    """
    print("Connected with result code", rc)
    for topic in TOPICS:
        client.subscribe(topic)
        print(f"Subscribed to {topic}")

def on_message(client, userdata, msg):
    """
    Callback function triggered when a subscribed MQTT message is received.
    Parses the payload using the process_payload() function and logs results.
    """
    try:
        # Decode the incoming JSON payload
        payload = json.loads(msg.payload.decode())

        # Process the payload into structured output
        result = process_payload(msg.topic, payload)

        # Extract Smartbike ID from topic (e.g., bike/000001/...)
        device_id = msg.topic.split('/')[1]

        # Log brake-specific messages
        if result["event"] == "brake":
            print(f"[{device_id}] Brake {result['status']} at {result['timestamp']}")

        # Log sensor telemetry values (speed, power, cadence)
        elif result["event"] in {"speed", "cadence", "power"}:
            print(f"[{device_id}] {result['event'].capitalize()}: {result['value']} {result.get('unit', '')} at {result['timestamp']}")

        # Log unknown or unsupported payloads
        else:
            print(f"[{device_id}] Unknown event: {result}")

    except Exception as e:
        # Handle payload parsing or topic errors gracefully
        print(f"Failed to parse message from {msg.topic}: {e}")

# Initialize MQTT client
client = mqtt.Client()

# Register connect and message callbacks
client.on_connect = on_connect
client.on_message = on_message

# Connect to the MQTT broker
client.connect(BROKER, PORT, 60)

# Start an infinite loop to receive and handle MQTT messages
client.loop_forever()
