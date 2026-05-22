"""
laudianto_agent.py — Kimberly, AI Agent untuk Laudianto Design Studio
======================================================================
Agent customer service hangat dan personal untuk Laudianto.
Melayani pertanyaan seputar jasa desain logo, brand identity, dan konten sosmed.

HOW TO RUN:
1. Pastikan sudah install:  pip install google-genai
2. Isi API key kamu di bawah (baris 24)
3. Isi harga jasa di bagian PRICE LIST (baris 50-60)
4. Jalankan:                python laudianto_agent.py
"""

from google import genai
from google.genai import types

# ---------------------------------------------------------------
# STEP 1: API Key kamu
# ---------------------------------------------------------------
API_KEY = "AIzaSyDX8FsQoP-nHWHNHbUTXznkYKpc582xgdM"

# ---------------------------------------------------------------
# STEP 2: PRICE LIST — Isi harga sesuai yang berlaku di Laudianto
# ---------------------------------------------------------------
SERVICES = """
LAYANAN & HARGA LAUDIANTO:

1. Logo Design
   - Logo Basic      : Rp [25000] — 1 konsep, 2x revisi
   - Logo Standard   : Rp [50000] — 3 konsep, 5x revisi
   - Logo Premium    : Rp [100000] — unlimited konsep & revisi

2. Brand Identity Package
   - Starter Pack    : Rp [100000] — logo + warna + tipografi
   - Full Pack       : Rp [500000] — starter + business card + kop surat + panduan brand

3. Social Media Content
   - 1 Post          : Rp [50000]
   - Paket 10 Post   : Rp [250000]
   - Paket 30 Post   : Rp [499000] (1 bulan penuh)

PROSES ORDER:
- DP 50% di awal sebelum pengerjaan dimulai
- Pelunasan sebelum file final dikirim
- Estimasi pengerjaan diinformasikan saat konfirmasi order

PEMBAYARAN:
- Transfer Bank: BCA / Mandiri / BRI / BNI
- QRIS (scan & bayar, semua e-wallet bisa)

KONTAK & PORTFOLIO:
- WhatsApp  : [+62895241118755]
- Instagram : [laudianto]
- Portfolio : [https://www.linkedin.com/in/jimmyliedianto/]
"""

# ---------------------------------------------------------------
# STEP 3: Kepribadian Kimberly
# ---------------------------------------------------------------
SYSTEM_PROMPT = f"""
Kamu adalah Kimberly, asisten virtual yang hangat, personal, dan penuh perhatian
untuk Laudianto Design Studio — jasa desain grafis profesional yang melayani
seluruh Indonesia secara online.

Kamu membantu calon klien dan klien yang sudah ada dengan pertanyaan seputar
layanan desain, harga, proses order, dan hal-hal umum lainnya.

{SERVICES}

PANDUAN CARA MENJAWAB:
- Gunakan Bahasa Indonesia yang hangat dan terasa personal — seperti berbicara
  dengan teman yang profesional, bukan robot
- Sapa dengan ramah di awal percakapan
- Jika ada yang bertanya harga, jelaskan dengan lengkap dan tawarkan untuk diskusi
  lebih lanjut sesuai kebutuhan mereka
- Jika ada yang mau order, arahkan langsung ke WhatsApp atau Instagram Laudianto
- Jika ada pertanyaan yang tidak kamu tahu jawabannya, jujur saja dan sarankan
  menghubungi langsung tim Laudianto via WhatsApp
- Boleh pakai emoji sesekali agar terasa lebih hangat 😊
- Jangan terlalu panjang — jawab to the point tapi tetap ramah
- Selalu tawarkan bantuan lebih di akhir pesan

INGAT: Kamu adalah wajah pertama Laudianto. Buat setiap klien merasa dihargai
dan yakin bahwa mereka berada di tangan yang tepat.
"""

# ---------------------------------------------------------------
# STEP 4: Jalankan Kimberly
# ---------------------------------------------------------------
def run_agent():
    """Jalankan agent Kimberly di terminal."""

    client = genai.Client(api_key=API_KEY)

    chat = client.chats.create(
        model="models/gemini-3.5-flash",
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT
        )
    )

    print("=" * 60)
    print("  Halo! Selamat datang di Laudianto Design Studio 🎨")
    print("  Saya Kimberly, siap membantu kamu hari ini.")
    print("  (Ketik 'keluar' untuk mengakhiri percakapan)")
    print("=" * 60)
    print()

    while True:
        user_input = input("Kamu: ").strip()

        if user_input.lower() in ["keluar", "exit", "quit", "bye"]:
            print("\nKimberly: Terima kasih sudah menghubungi Laudianto! 💛")
            print("          Semoga harimu menyenangkan. Sampai jumpa!")
            break

        if not user_input:
            continue

        try:
            response = chat.send_message(user_input)
            print(f"\nKimberly: {response.text}\n")

        except Exception as e:
            error_message = str(e)
            if "invalid" in error_message.lower() or "401" in error_message or "API_KEY" in error_message:
                print("\n[ERROR] API key tidak valid. Cek kembali baris 24.")
                break
            else:
                print(f"\n[ERROR] {error_message}\n")
                break


if __name__ == "__main__":
    run_agent()
