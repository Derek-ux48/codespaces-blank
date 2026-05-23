import os
import base64
import io
import time
from flask import Flask, render_template, request, jsonify
import qrcode
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, template_folder='../templates')

MPESA_KEY = os.environ.get("MPESA_CONSUMER_KEY")
MPESA_SECRET = os.environ.get("MPESA_CONSUMER_SECRET")

def get_mpesa_token():
    """Generates an OAuth access token from the gateway endpoint"""
    api_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    try:
        auth_string = base64.b64encode(f"{MPESA_KEY}:{MPESA_SECRET}".encode()).decode()
        headers = {"Authorization": f"Basic {auth_string}"}
        response = requests.get(api_url, headers=headers)
        if response.status_code == 200:
            return response.json().get("access_token")
        return None
    except Exception as e:
        print(f"Auth Network Error: {e}")
        return None

def initiate_stk_push(token, phone, amount):
    """Packages the transaction details and fires the payment trigger request"""
    url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    
    # Structural parameters expected by financial gateways
    timestamp = time.strftime("%Y%m%d%H%M%S")
    business_short_code = "174379"  # Standard sandbox testing shortcode
    passkey = "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919"
    
    # Cryptographic password layer validation
    password_str = f"{business_short_code}{passkey}{timestamp}"
    password = base64.b64encode(password_str.encode()).decode()
    
    payload = {
        "BusinessShortCode": business_short_code,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": int(amount),
        "PartyA": phone,
        "PartyB": business_short_code,
        "PhoneNumber": phone,
        "CallBackURL": "https://mydomain.com/path", # Production needs live public link
        "AccountReference": "SwiftPayTerminal",
        "TransactionDesc": "POS Checkout Payment"
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        print(f"Network Gateway Response Status: {response.status_code}")
        print(f"Gateway Metadata: {response.text}")
        return response.json()
    except Exception as e:
        print(f"Gateway Communication Failure: {e}")
        return None

@app.route('/', methods=['GET', 'POST'])
def pos_terminal():
    qr_img = None
    amount = None

    if request.method == 'POST':
        amount = request.form.get('amount')
        phone = request.form.get('phone_number')
        
        if amount and phone:
            token = get_mpesa_token()
            if token:
                print(f"[Handshake] Token Verified: Secure channel open.")
                # Execute the payment processing dispatch
                stk_response = initiate_stk_push(token, phone, amount)
            
            # Keep generating the fallback visual system link
            qr_data = f"SwiftPay | Amt: {amount} | Phone: {phone} | Ref: {int(time.time())}"
            qr = qrcode.QRCode(version=1, box_size=10, border=4)
            qr.add_data(qr_data)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            buffer = io.BytesIO()
            img.save(buffer, format="PNG")
            qr_img = base64.b64encode(buffer.getvalue()).decode('utf-8')

    return render_template('index.html', qr_img=qr_img, amount=amount)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)