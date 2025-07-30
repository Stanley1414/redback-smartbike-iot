# MQTT Client for Smartbike Telemetry

This script listens for real-time MQTT messages from all Smartbike devices and parses key telemetry events such as speed, power, cadence, and brake state.

##  Topics Subscribed To

The mqtt_client uses MQTT wildcards to automatically work with any number of bikes:

- `bike/+/speed/report`
- `bike/+/power/report`
- `bike/+/cadence/report`
- `bike/+/button/report`

##  How It Works

- Connects to the Mosquitto MQTT broker at `10.137.0.149:1883`
- Subscribes to the above topics using wildcard (`+`)
- Delegates payload parsing to `process_payload()` in `mqtt_ingestor.py`
- Logs structured output to console:
  - Brake status (applied or released)
  - Telemetry values (speed, power, cadence)

##  How to Run

1. Ensure the MQTT broker is running and accessible at `10.137.0.149`.
2. Run the script:

```bash
python mqtt_client.py
```

##  Example Output

```
[000001] Brake applied at 1722834169.6
[000002] Speed: 5.9 m/s at 1722834172.1
[000003] Power: 125.0 W at 1722834173.4
```

##  Dependencies

This script requires the following Python package:

- `paho-mqtt`

Install it with:

```bash
pip install paho-mqtt
```

##  File Summary

| File | Purpose |
|------|---------|
| `mqtt_client.py` | Main MQTT subscriber for bike telemetry |
| `mqtt_ingestor.py` | Payload processor that returns structured data |