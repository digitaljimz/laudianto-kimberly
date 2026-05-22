"""
starter_agent.py — Your First Agentic AI (FREE version using Google Gemini)
============================================================================
This is a simple customer service agent that responds in Bahasa Indonesia.
It remembers the conversation history so it can reply in context.

HOW TO RUN:
1. Install the library:    pip install google-genai
2. Set your API key:       Replace "YOUR_API_KEY_HERE" below with your key
                           Get your FREE key at: https://aistudio.google.com
3. Run it:                 python starter_agent.py
"""

from google import genai
from google.genai import types

# ---------------------------------------------------------------
# STEP 1: Set your FREE API key
# Get this from https://aistudio.google.com -> click "Get API Key"
# No credit card needed!
# ---------------------------------------------------------------
API_KEY = "AIzaSyDisvjuxsiJ2X6OSfHw2oEskHGmWcViOM8"

# ---------------------------------------------------------------
# STEP 2: Define your agent's personality with a system prompt
# This is the most powerful part — change this to change behavior!
# ---------------------------------------------------------------
SYSTEM_PROMPT = """
Kamu adalah Sari, asisten customer service yang ramah dan profesional untuk Toko Maju,
sebuah toko online yang menjual pakaian wanita.

Informasi toko:
- Jam operasional: Senin-Sabtu, 08.00-21.00 WIB
- Pengiriman: JNE, J&T, SiCepat
- Pembayaran: Transfer bank, GoPay, OVO, Dana, COD (khusus Jabodetabek)
- Retur: Bisa dalam 3 hari setelah barang diterima, asalkan belum dipakai

Produk unggulan:
- Gamis premium: Rp 250.000 - Rp 450.000
- Hijab segi empat: Rp 75.000 - Rp 150.000
- Set baju kondangan: Rp 350.000 - Rp 600.000

Selalu jawab dengan:
- Bahasa Indonesia yang sopan dan ramah
- Sapa pelanggan dengan hangat
- Tawarkan bantuan lebih lanjut di akhir pesan
- Jika pertanyaan di luar kemampuanmu, sarankan menghubungi admin di WA: 0812-3456-7890
"""

# ---------------------------------------------------------------
# STEP 3: The main agent loop
# ---------------------------------------------------------------
def run_agent():
    """Run the customer service agent in the terminal."""

    # Initialize the Gemini client with your API key
    client = genai.Client(api_key=API_KEY)

    # Start a chat session with the system prompt
    chat = client.chats.create(
        model="models/gemini-3.5-flash",
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT
        )
    )

    print("=" * 60)
    print("  Selamat datang di Toko Maju!")
    print("  Asisten kami siap membantu Anda.")
    print("  (Ketik 'keluar' untuk mengakhiri percakapan)")
    print("=" * 60)
    print()

    while True:
        # Get input from the user
        user_input = input("Anda: ").strip()

        # Exit condition
        if user_input.lower() in ["keluar", "exit", "quit", "bye"]:
            print("\nSari: Terima kasih sudah menghubungi Toko Maju!")
            print("      Semoga harimu menyenangkan. Sampai jumpa!")
            break

        # Skip empty input
        if not user_input:
            continue

        # Send message to Gemini and get a response
        try:
            response = chat.send_message(user_input)
            assistant_reply = response.text
            print(f"\nSari: {assistant_reply}\n")

        except Exception as e:
            error_message = str(e)
            if "API_KEY" in error_message or "invalid" in error_message.lower() or "401" in error_message:
                print("\n[ERROR] API key tidak valid.")
                print("Pastikan kamu sudah mengisi API_KEY dengan benar di baris 23.")
                print("Dapatkan API key GRATIS di: https://aistudio.google.com\n")
                break
            else:
                print(f"\n[ERROR] Terjadi kesalahan: {error_message}\n")
                break


# ---------------------------------------------------------------
# STEP 4: Run the agent
# ---------------------------------------------------------------
if __name__ == "__main__":
    run_agent()


# ---------------------------------------------------------------
# NEXT STEPS — Things to try once this is working:
# ---------------------------------------------------------------
# 1. Change SYSTEM_PROMPT to match a real business you know
# 2. Add a product list that the agent can "look up"
# 3. Try asking it edge-case questions ("Ada diskon?", "Bisa nego?")
# 4. Connect it to a real WhatsApp number using Twilio
# ---------------------------------------------------------------
