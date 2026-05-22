from flask import Flask, render_template, request
import qrcode
import io
import base64
import time
from security import generate_secure_hash

app = Flask(__name__, template_folder='../templates')

@app.route('/', methods=['GET', 'POST'])
def pos_terminal():
    qr_img = None
    amount = None
    
    if request.method == 'POST':
        amount = request.form.get('amount')
        till_number = "554433"
        reference = f"INV_{int(time.time())}"
        
        # 1. Apply your Cybersecurity Signature
        signature = generate_secure_hash(amount, till_number, reference)
        
        # 2. Build the live payment payload data
        qr_data = f"LipaNaMpesa://Till={till_number}&Amount={amount}&Ref={reference}&Sign={signature[:10]}"
        
        # 3. Generate the actual visual QR Code image
        qr = qrcode.QRCode(version=1, box_size=10, border=4)
        qr.add_data(qr_data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Convert image to a format the web page can read instantly
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        qr_img = base64.b64encode(buf.getvalue()).decode('utf-8')
        
    return render_template('index.html', qr_img=qr_img, amount=amount)

if __name__ == '__main__':
    # Render assigns a dynamic port, default to 5000 locally
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
