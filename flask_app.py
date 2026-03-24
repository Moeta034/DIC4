from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
DB_NAME = 'aiotdb.db'

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS sensors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            device_id TEXT,
            ip_address TEXT,
            temp REAL,
            humd REAL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/health', methods=['GET'])
def health_check():
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>API Health Status</title>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
            body {
                margin: 0;
                padding: 0;
                font-family: 'Inter', sans-serif;
                background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
                color: #ffffff;
                display: flex;
                height: 100vh;
                justify-content: center;
                align-items: center;
                overflow: hidden;
            }
            .container {
                background: rgba(255, 255, 255, 0.05);
                backdrop-filter: blur(15px);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 20px;
                padding: 50px 80px;
                text-align: center;
                box-shadow: 0 20px 50px rgba(0, 0, 0, 0.5);
                animation: fadeIn 1s ease-out;
            }
            h1 {
                font-size: 3rem;
                margin-bottom: 10px;
                background: linear-gradient(to right, #00c6ff, #0072ff);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }
            p {
                font-size: 1.2rem;
                color: #b0c4de;
                margin-top: 0;
            }
            .status-indicator {
                display: inline-block;
                width: 20px;
                height: 20px;
                background-color: #00ff88;
                border-radius: 50%;
                margin-right: 15px;
                box-shadow: 0 0 20px #00ff88;
                animation: pulse 1.5s infinite;
            }
            .status-wrapper {
                display: flex;
                align-items: center;
                justify-content: center;
                margin-bottom: 20px;
            }
            @keyframes pulse {
                0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(0, 255, 136, 0.7); }
                70% { transform: scale(1); box-shadow: 0 0 0 15px rgba(0, 255, 136, 0); }
                100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(0, 255, 136, 0); }
            }
            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(20px); }
                to { opacity: 1; transform: translateY(0); }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="status-wrapper">
                <div class="status-indicator"></div>
                <h1>System Online</h1>
            </div>
            <p>AIoT Flask Server is running perfectly.</p>
        </div>
    </body>
    </html>
    """
    return html_content

@app.route('/sensor', methods=['POST'])
def receive_sensor_data():
    data = request.json
    if not data:
        return jsonify({"error": "No JSON payload"}), 400
    
    device_id = data.get('device_id', 'unknown')
    ip_address = data.get('ip_address', '0.0.0.0')
    temp = data.get('temp')
    humd = data.get('humd')
    
    if temp is None or humd is None:
        return jsonify({"error": "Missing temp or humd"}), 400
        
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO sensors (device_id, ip_address, temp, humd) VALUES (?, ?, ?, ?)",
              (device_id, ip_address, temp, humd))
    conn.commit()
    conn.close()
    
    return jsonify({"status": "success", "message": "Data inserted"}), 201

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)
