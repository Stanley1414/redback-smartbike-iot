# Payload Processor for Smartbike MQTT Messages
# This module transforms raw MQTT payloads into structured telemetry or event logs.

def process_payload(topic, payload):
    """
    Parses the incoming MQTT payload and extracts meaningful event information
    based on the topic and payload structure.

    Args:
        topic (str): The full MQTT topic string (e.g., "bike/000001/speed/report")
        payload (dict): The decoded JSON payload received from MQTT

    Returns:
        dict: A structured dictionary containing:
              - event: the type of event (e.g., "brake", "speed", etc.)
              - value/status: depending on event type
              - timestamp: when the event was recorded
    """

    # Handle brake button event
    if "button" in payload and payload["button"] == "BREAK":
        return {
            "event": "brake",
            "status": "applied" if payload["state"] == 1 else "released",
            "timestamp": payload["timestamp"]
        }

    # Handle telemetry data (speed, cadence, power, etc.)
    elif "value" in payload:
        return {
            "event": topic.split('/')[-2],  # Extract event type from topic (e.g., "speed")
            "value": payload["value"],
            "unit": payload.get("unitName"),  # Optional unit (e.g., "RPM", "W")
            "timestamp": payload["timestamp"]
        }

    # Catch-all for unexpected or unsupported payloads
    else:
        return {
            "event": "unknown",
            "payload": payload  # Return the raw payload for debugging/logging
        }
