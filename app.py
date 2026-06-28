from flask import Flask, request, Response
import requests

app = Flask(__name__)

@app.route('/')
def proxy():
    target_url = request.args.get('url')
    if not target_url:
        return "Missing ?url= parameter", 400
    
    try:
        # स्ट्रीम=ट्रू ताकि बड़ी इमेज सीधे पास हो सके
        resp = requests.get(target_url, stream=True)
        return Response(resp.iter_content(chunk_size=10*1024), 
                        content_type=resp.headers.get('Content-Type', 'image/jpeg'),
                        status=resp.status_code)
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
