from django.urls import re_path
from device_manager.sensor_data_ws import SensorDataConsumer

websocket_urlpatterns = [
    re_path(r'ws/sensor/(?P<type>[-\w]+)', SensorDataConsumer.as_asgi()),
]
