import paho.mqtt.publish as publish

publish.single("yuyao/server", "payload", hostname="0.0.0.0")
