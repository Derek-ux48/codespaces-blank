# SwiftPay Dynamic QR Merchant Terminal

A lightweight, high-performance web-based Point of Sale (POS) system designed for fast-paced commercial retail hubs. This system streamlines business transactions by dynamically encoding checkout bill totals into secure, instantly scannable data formats, removing the risk of manual input errors.

## 🚀 Live Deployment
Experience the live cloud application here: [SwiftPay Terminal](https://swiftpay-terminal.onrender.com)

## 🛠️ Tech Stack & Architecture
- **Backend Framework:** Python 3 with Flask (Configured for dynamic web routing and environment production handling).
- **Core Engine:** Real-time visual data parsing via Python `qrcode` and `Pillow` image processing layers.
- **Deployment Pipeline:** Integrated CI/CD automation mapped directly via Git version control to Render cloud containers.

## 🔒 Engineering & Security Highlights
- **Dynamic Port Management:** Implemented dynamic binding configurations via `os.environ.get("PORT")` to seamlessly transition between local test scripts and Linux-based cloud infrastructure environments.
- **Production Error Resolution:** Successfully diagnosed and resolved cloud runtime exit status constraints (Exit codes 1, 2, and 127) through environment and path realignment.
- **Zero-Footprint Client Target:** Structured purely as an cross-platform web application to ensure compatibility across entry-level merchant hardware without requiring storage-heavy native app installations.
