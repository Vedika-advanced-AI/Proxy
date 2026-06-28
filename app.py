from flask import Flask, request, Response
import requests
from apscheduler.schedulers.background import BackgroundScheduler
import os

app = Flask(__name__)

# आपका रेंडर URL
RENDER_URL = "https://proxy-kyne.onrender.com"

# 'Time Robot' फंक्शन
def ping_server():
    print("Time Robot: Pinging server to stay awake...")
    try:
        # अब यह नए '/ping' रास्ते पर पिंग करेगा
        requests.get(f"{RENDER_URL}/ping", timeout=10)
        print("Time Robot: Ping successful! Server is awake.")
    except Exception as e:
        print(f"Time Robot Error: {e}")

# शेड्यूलर सेटअप (हर 10 मिनट में पिंग)
scheduler = BackgroundScheduler()
scheduler.add_job(func=ping_server, trigger="interval", minutes=10)
scheduler.start()

# 1. नया और खास पिंग (Ping) रूट
@app.route('/ping')
def keep_alive():
    return "I am awake, Divy Patel!", 200

# 2. आपका मेन इमेज प्रॉक्सी रूट
@app.route('/')
def proxy():
    target_url = request.args.get('url')
    if not target_url:
        return "Missing ?url= parameter", 400
    
    try:
        # पॉलिनेशंस से इमेज फेच करना
        resp = requests.get(target_url, stream=True, timeout=60)
        
        return Response(
            resp.iter_content(chunk_size=10*1024), 
            content_type=resp.headers.get('Content-Type', 'image/jpeg'),
            status=resp.status_code
        )
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
