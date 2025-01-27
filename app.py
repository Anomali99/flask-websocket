from flask import Flask, render_template, request, jsonify
from flask_sock import Sock
import json

app = Flask(__name__)
sock = Sock(app)

# Variabel global untuk menyimpan status relay dan data sensor
sensor_data = {"temperature": None, "humidity": None}
relay_status = {"relay": False}
ws_clients = set()

@app.route('/')
def index():
    return render_template('index.html')

@sock.route('/sensor')
def sensor(ws):
    global sensor_data
    while True:
        try:
            data = ws.receive()
            if data:
                sensor_data = json.loads(data)  # Gunakan json.loads
                print(f"Received sensor data: {sensor_data}")
                for client in list(ws_clients):
                    try:
                        client.send(json.dumps(sensor_data))
                    except Exception:
                        ws_clients.remove(client)
                ws.send("Data received")
        except Exception as e:
            print(f"Error in WebSocket communication: {e}")
            break

@app.route('/relay', methods=['POST'])
def control_relay():
    global relay_status
    relay_status["relay"] = request.json.get("relay", False)
    return jsonify(relay_status), 200

@sock.route('/sensor_data')
def get_sensor_data(ws):
    ws_clients.add(ws)
    try:
        while True:
            ws.receive()
    except Exception:
        pass
    finally:
        ws_clients.remove(ws)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
