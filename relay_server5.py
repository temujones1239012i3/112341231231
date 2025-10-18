from flask import Flask
from flask_cors import CORS
import logging
import os
import re

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
# Validation
# ============================================================
def is_valid_game_id(game_id):
    """Check if the game_id is valid (UUID or long hex string)."""
    # UUID format: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx (36 chars)
    uuid_pattern = r'^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$'
    
    # Long hex format: 64+ hexadecimal characters
    hex_pattern = r'^[a-fA-F0-9]{64,}$'
    
    if re.match(uuid_pattern, game_id, re.IGNORECASE):
        return True
    if re.match(hex_pattern, game_id):
        return True
    
    return False

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
    
    if is_valid_game_id(game_id):
        latest_id = game_id
        print(f"✅ New ID: {game_id}")
        return "OK"
    
    print(f"❌ Invalid ID rejected: {game_id} (length: {len(game_id)})")
    return "Invalid ID", 400

@app.route('/clear')
def clear():
    """Clear the current ID."""
    global latest_id
    latest_id = None
    print("🗑️ ID cleared")
    return "OK"

@app.route('/')
def home():
    """Status page."""
    id_display = latest_id if latest_id else 'Waiting for game instance...'
    id_length = len(latest_id) if latest_id else 0
    id_type = ""
    
    if latest_id:
        if len(latest_id) == 36:
            id_type = " (UUID)"
        else:
            id_type = f" (Hex, {id_length} chars)"
    
    return f"""
    <html>
    <head>
        <meta http-equiv="refresh" content="2">
        <style>
            body {{
                background: #0d1117;
                color: #58a6ff;
                font-family: monospace;
                padding: 40px;
                text-align: center;
            }}
            h1 {{ color: #58a6ff; }}
            #id {{
                font-size: 18px;
                padding: 20px;
                background: #161b22;
                border-radius: 8px;
                margin: 20px auto;
                max-width: 800px;
                word-break: break-all;
            }}
            .info {{
                color: #8b949e;
                font-size: 14px;
                margin-top: 10px;
            }}
        </style>
    </head>
    <body>
        <h1>🎮 Game Instance Relay</h1>
        <div id="id">{id_display}</div>
        <div class="info">{id_type}</div>
        <p style="color: #8b949e; font-size: 14px;">Auto-refreshes every 2 seconds</p>
    </body>
    </html>
    """

# ============================================================
# Run
# ============================================================
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    print("🚀 Relay Server Running on port", port)
    print("📋 Accepts: UUID (36 chars) and Hex IDs (64+ chars)")
    app.run(host='0.0.0.0', port=port, debug=False)