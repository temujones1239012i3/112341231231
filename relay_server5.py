from flask import Flask
from flask_cors import CORS
import logging
import os
app = Flask(__name__)
CORS(app)
# Disable Flask logging spam
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
# ============================================================
# State
# ============================================================
latest_id = None
# ============================================================
# Routes
# ============================================================
@app.route('/latest')
def get_latest():
    """Get the latest game instance ID."""
    global latest_id
    return latest_id if latest_id else "", 200, {'Content-Type': 'text/plain'}
@app.route('/post/<game_id>')
def post_id(game_id):
    """Post a new game instance ID."""
    global latest_id
    if len(game_id) == 36:
        latest_id = game_id
        print(f"✅ New ID: {game_id}")
        return "OK"
    return "Invalid ID", 400
@app.route('/clear')
def clear():
    """Clear the current ID."""
    global latest_id
    latest_id = None
    return "OK"
@app.route('/')
def home():
    """Status page."""
    return f"""
    <html>
    <head>
        <meta http-equiv="refresh" content="2">
        <style>
            body {{
                background: 
#0d1117;
                color: 
#58a6ff;
                font-family: monospace;
                padding: 40px;
                text-align: center;
            }}
            h1 {{ color: 
#58a6ff; }}
            #id {{
                font-size: 24px;
                padding: 20px;
                background: 
#161b22;
                border-radius: 8px;
                margin: 20px auto;
                max-width: 600px;
                word-break: break-all;
            }}
        </style>
    </head>
    <body>
        <h1>🎮 Game Instance Relay</h1>
        <div id="id">{latest_id if latest_id else 'Waiting for game instance...'}</div>
        <p style="color: 
#8b949e; font-size: 14px;">Auto-refreshes every 2 seconds</p>
    </body>
    </html>
    """
# ============================================================
# Run
# ============================================================
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    print("🚀 Relay Server Running on port", port)
    app.run(host='0.0.0.0', port=port, debug=False)