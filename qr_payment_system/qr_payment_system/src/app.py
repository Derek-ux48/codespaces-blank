import os
import base64
import io
import time
from flask import Flask, render_template, request
import qrcode
from dotenv import load_dotenv

# Initialize environment variables securely
load_dotenv()

app = Flask(__name__, template_folder='../templates')

# Pull secure keys from our hidden .env configuration layer
MPESA_KEY = os.environ.get("MPESA_CONSUMER_KEY")
MPESA_SECRET = os.environ.get("MPESA_CONSUMER_SECRET")

@app.route('/', methods=['GET', 'POST'])
def pos_terminal():
    qr_img = None
    amount = None

    if request.method == 'POST':
        amount = request.form.get('amount')
        if amount:
            # Structuring the payload architecture for Phase 2 gateway handshake
            # For now, we dynamically encode the bill total into the terminal UI
            qr_data = f"SwiftPay Merchant Terminal | Amount: KES {amount} | Ref: {int(time.time())}"
            
            qr = qrcode.QRCode(version=1, box_size=10, border=4)
            qr.add_data(qr_data)
            qr.make(fit=True)
            
            img = qr.make_image(fill_color="black", back_color="white")
            
            buffer = io.BytesIO()
            img.save(buffer, format="PNG")
            qr_bytes = buffer.getvalue()
            
            qr_img = base64.b64encode(qr_bytes).decode('utf-8')

    return render_template('index.html', qr_img=qr_img, amount=amount)

if __name__ == '__main__':
    # Render assigns a dynamic cloud port, defaulting to 5000 locally
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
