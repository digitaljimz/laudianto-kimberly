"""
app.py — Kimberly Web Server untuk Laudianto Design Studio
===========================================================
Supports both Twilio (WhatsApp sandbox) and Fonnte.

CARA KERJA (Twilio):
  WhatsApp → Twilio → /twilio (webhook) → Gemini → TwiML reply → Twilio → WhatsApp

CARA JALANKAN (lokal untuk testing):
  1. pip install -r requirements.txt
  2. Isi file .env dengan API key kamu
  3. python app.py
  4. Server berjalan di http://localhost:5000
"""

import os
import requests
from flask import Flask, request, jsonify
from google import genai
from google.genai import types
from dotenv import load_dotenv
from twilio.twiml.messaging_response import MessagingResponse

# Load API keys dari file .env
load_dotenv()

app = Flask(__name__)

# ---------------------------------------------------------------
# KONFIGURASI
# ---------------------------------------------------------------
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
FONNTE_TOKEN   = os.getenv("FONNTE_TOKEN", "")

# ---------------------------------------------------------------
# PRICE LIST & INFO LAYANAN LAUDIANTO
# ---------------------------------------------------------------
SERVICES = """
LAYANAN & HARGA LAUDIANTO:

1. Logo Design
   - Logo Basic      : Rp [ISI HARGA] — 1 konsep, 2x revisi
   - Logo Standard   : Rp [ISI HARGA] — 3 konsep, 5x revisi
   - Logo Premium    : Rp [ISI HARGA] — unlimited konsep & revisi

2. Brand Identity Package
   - Starter Pack    : Rp [ISI HARGA] — logo + warna + tipografi
   - Full Pack       : Rp [ISI HARGA] — starter + business card + kop surat + panduan brand

3. Social Media Content
   - 1 Post          : Rp [ISI HARGA]
   - Paket 10 Post   : Rp [ISI HARGA]
   - Paket 30 Post   : Rp [ISI HARGA] (1 bulan penuh)

PROSES ORDER:
- DP 50% di awal sebelum pengerjaan dimulai
- Pelunasan sebelum file final dikirim
- Estimasi pengerjaan diinformasikan saat konfirmasi order

PEMBAYARAN:
- Transfer Bank: BCA / Mandiri / BRI / BNI
- QRIS (scan & bayar, semua e-wallet bisa)

KONTAK & PORTFOLIO:
- WhatsApp  : [ISI NOMOR WA LAUDIANTO]
- Instagram : [ISI USERNAME IG LAUDIANTO]
- Portfolio : [ISI LINK PORTFOLIO JIKA ADA]
"""

# ---------------------------------------------------------------
# KEPRIBADIAN KIMBERLY
# ---------------------------------------------------------------
SYSTEM_PROMPT = f"""
Kamu adalah Kimberly, asisten virtual yang hangat, personal, dan penuh perhatian
untuk Laudianto Design Studio — jasa desain grafis profesional yang melayani
seluruh Indonesia secara online.

{SERVICES}

PANDUAN CARA MENJAWAB:
- Gunakan Bahasa Indonesia yang hangat dan terasa personal
- Sapa dengan ramah di awal percakapan
- Jika ada yang bertanya harga, jelaskan dengan lengkap
- Jika ada yang mau order, arahkan ke WhatsApp atau Instagram Laudianto
- Jika tidak tahu jawabannya, jujur dan sarankan hubungi tim langsung
- Boleh pakai emoji sesekali
- Jawab to the point tapi tetap ramah
- Selalu tawarkan bantuan lebih di akhir pesan
"""

# ---------------------------------------------------------------
# MEMORY — riwayat percakapan per nomor WhatsApp
# ---------------------------------------------------------------
conversation_histories = {}

gemini_client = None


def get_gemini_reply(sender_number: str, user_message: str) -> str:
    """Kirim pesan ke Gemini, simpan histori per nomor pengirim."""
    global gemini_client
    if gemini_client is None:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            return "Maaf, konfigurasi sistem belum lengkap. Hubungi admin ya!"
        gemini_client = genai.Client(api_key=api_key)
    if sender_number not in conversation_histories:
        conversation_histories[sender_number] = gemini_client.chats.create(
            model="models/gemini-3.5-flash",
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT
            )
        )
    chat = conversation_histories[sender_number]
    try:
        response = chat.send_message(user_message)
        return response.text
    except Exception as e:
        print(f"[ERROR Gemini] {e}")
        return f"DEBUG ERROR: {str(e)}"


# ---------------------------------------------------------------
# ENDPOINTS
# ---------------------------------------------------------------

@app.route("/", methods=["GET"])
def home():
    """Health check."""
    return jsonify({
        "status": "running",
        "agent": "Kimberly — Laudianto Design Studio",
        "message": "Server aktif dan siap menerima pesan WhatsApp!"
    })


@app.route("/twilio", methods=["POST"])
def twilio_webhook():
    """
    Webhook untuk Twilio WhatsApp Sandbox.
    Twilio mengirim pesan masuk ke sini, kita balas dengan format TwiML.
    Daftarkan URL ini di Twilio console sebagai:
      https://your-app.up.railway.app/twilio
    """
    # Twilio mengirim data sebagai form POST
    sender  = request.form.get("From", "unknown")   # format: whatsapp:+62xxxxxxx
    message = request.form.get("Body", "").strip()

    print(f"[TWILIO] Dari: {sender} | Pesan: {message}")

    # Dapatkan balasan Kimberly
    reply = get_gemini_reply(sender, message)
    print(f"[Kimberly → {sender}] {reply}")

    # Kirim balik dalam format TwiML (yang Twilio butuhkan)
    twiml = MessagingResponse()
    twiml.message(reply)
    return str(twiml), 200, {"Content-Type": "text/xml"}


@app.route("/webhook", methods=["POST"])
def fonnte_webhook():
    """Webhook untuk Fonnte (untuk nanti jika upgrade ke Fonnte)."""
    data    = request.json or request.form.to_dict()
    sender  = data.get("sender", "unknown")
    message = data.get("message", "")
    if not message:
        return jsonify({"status": "ignored"})
    reply = get_gemini_reply(sender, message)
    if FONNTE_TOKEN:
        requests.post(
            "https://api.fonnte.com/send",
            headers={"Authorization": FONNTE_TOKEN},
            data={"target": sender, "message": reply, "countryCode": "62"}
        )
    return jsonify({"status": "ok", "reply": reply})


@app.route("/test", methods=["GET"])
def test():
    """Test Kimberly di browser tanpa WhatsApp."""
    pesan  = request.args.get("pesan", "Halo!")
    sender = request.args.get("nomor", "test_user")
    reply  = get_gemini_reply(sender, pesan)
    return jsonify({"kamu": pesan, "kimberly": reply})


# ---------------------------------------------------------------
# JALANKAN SERVER
# ---------------------------------------------------------------
if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    print(f"\nKimberly siap di http://localhost:{port}")
    print(f"Test: http://localhost:{port}/test?pesan=Harga+logo+berapa?\n")
    app.run(host="0.0.0.0", port=port, debug=True)
