from flask import Flask, render_template, request, jsonify
from firebase_admin import credentials, messaging
from flask_cors import CORS
from flask_sock import Sock
import json, firebase_admin

app = Flask(__name__)
sock = Sock(app)
CORS(app, resources={
    r"/*": {
        "origins": ["https://chat.anomali99.my.id"],
        "allow_headers": ["Content-Type", "Authorization"],
        "methods": ["GET", "POST", "OPTIONS"]
    }
})
cred = credentials.Certificate("./serviceAccountKey.json")
firebase_admin.initialize_app(cred)

sensor_data = {"moisture": 0, "temperature": 0, "humidity": 0, "lux": 0}
relay_status = {"relay": False}
ws_clients = set()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/notification/send', methods=['POST'])
def send_notification():
    try:
        body = request.json
        
        message = messaging.Message(
            notification=messaging.Notification(
                title=body['title'].strip(),
                body=body['message'].strip()
            ),
            token=body['targetToken'].strip()
        )

        response = messaging.send(message)
        print(response)
        
        return jsonify({
            "data":{
                "message" : "Success send notification"
            }
        })
        
    except Exception as e:
        print(e)
        return jsonify({
            "data":{
                "message" : "Failed send notification",
                "err": str(e)
            }
        }), 500

@app.route('/relay', methods=['POST'])
def control_relay():
    global relay_status
    relay_status["relay"] = request.json.get("relay", False)
    return jsonify(relay_status), 200

@sock.route('/sensor')
def sensor(ws):
    global sensor_data
    global relay_status
    while True:
        try:
            data = ws.receive()
            if data:
                request = json.loads(data)
                sensor_data = {
                    "moisture": request['moisture'], 
                    "temperature": request['temperature'], 
                    "humidity": request['humidity'], 
                    "lux": request['lux']
                } 
                # relay_status = {
                #     "relay": request['relay']
                # }
                print(f"Received sensor data: {sensor_data}")
                for client in list(ws_clients):
                    try:
                        client.send(json.dumps(sensor_data))
                    except Exception:
                        ws_clients.remove(client)
                ws.send(json.dumps(relay_status))
        except Exception as e:
            print(f"Error in WebSocket communication: {e}")
            break

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
    app.run(host='0.0.0.0', debug=False, port=5000)
