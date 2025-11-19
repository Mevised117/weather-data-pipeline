import requests
import json
from datetime import datetime
from google.cloud import bigquery
from google.oauth2 import service_account

# ==========================================
# ⚙️ ส่วนตั้งค่า (แก้ตรงนี้ให้เป็นของตัวเอง)
# ==========================================
API_KEY = "3e239c0e823ec74c848a709eec04db19"  # คีย์ OpenWeather (จาก Part 1)
CITY_NAME = "Bangkok"
# KEY_FILE_PATH = "weather-data-project-478717-7a4bd5cd309c.json"  # ชื่อไฟล์กุญแจที่เราโหลดมา
KEY_FILE_PATH = "key.json"  # ชื่อไฟล์กุญแจที่เราโหลดมา


# ดู Project ID จากหน้า Google Cloud มุมบนซ้าย
# จากรูปที่คุณส่งมา น่าจะเป็น 'weather-data-project-478717' (ลองเช็คดูอีกทีนะครับ)
PROJECT_ID = "weather-data-project-478717" 
DATASET_ID = "weather_schema"
TABLE_ID = "daily_weather"

# ==========================================
# 1. EXTRACT: ดึงข้อมูลจาก API
# ==========================================
def get_weather_data():
    print(f"📡 กำลังดึงข้อมูลสภาพอากาศของ {CITY_NAME}...")
    url = f"https://api.openweathermap.org/data/2.5/weather?q={CITY_NAME}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    
    if response.status_code == 200:
        print("✅ ดึงข้อมูลสำเร็จ!")
        return response.json()
    else:
        print("❌ ดึงข้อมูลพลาด:", response.text)
        return None

# ==========================================
# 2. TRANSFORM: จัดระเบียบข้อมูล
# ==========================================
def transform_data(raw_data):
    if not raw_data:
        return None
    
    print("🧹 กำลังจัดระเบียบข้อมูล...")
    # ดึงเฉพาะที่เราต้องการ ให้ตรงกับ Schema ใน BigQuery
    record = {
        "city": raw_data["name"],
        "temp": raw_data["main"]["temp"],
        "humidity": raw_data["main"]["humidity"],
        # แปลงเวลาปัจจุบันให้เป็น Format ที่ BigQuery เข้าใจ
        "timestamp": datetime.now().isoformat()
    }
    return record

# ==========================================
# 3. LOAD: ส่งขึ้น BigQuery (แบบ Batch Load - ฟรี)
# ==========================================
def load_to_bigquery(data):
    if not data:
        return

    print("🚀 กำลังส่งข้อมูลขึ้น Google BigQuery (แบบ Load Job)...")
    
    # 1. สร้างการเชื่อมต่อ
    credentials = service_account.Credentials.from_service_account_file(KEY_FILE_PATH)
    client = bigquery.Client(credentials=credentials, project=PROJECT_ID)

    # 2. ระบุเป้าหมาย
    table_ref = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}"

    # 3. ตั้งค่าการโหลด (ให้ต่อท้ายข้อมูลเดิม)
    job_config = bigquery.LoadJobConfig(
        write_disposition="WRITE_APPEND", 
    )

    # 4. ส่งข้อมูล (Load Job)
    # วิธีนี้คือการสร้าง Job เพื่อโหลดข้อมูล ซึ่งทำได้ฟรีใน Free Tier
    try:
        job = client.load_table_from_json(
            [data], # ข้อมูลต้องเป็น List
            table_ref,
            job_config=job_config
        )
        
        # รอให้ Job ทำงานเสร็จ (สำคัญมาก)
        job.result() 
        
        print(f"🎉 สำเร็จ! โหลดข้อมูลไปยังตาราง {TABLE_ID} เรียบร้อยแล้ว")
        print(f"ข้อมูลที่ส่งไป: {data}")
        
    except Exception as e:
        print("❌ เกิดข้อผิดพลาดในการส่งข้อมูล:", e)

# ==========================================
# 🔥 สั่งให้ทำงาน
# ==========================================
if __name__ == "__main__":
    # รันทีละขั้นตอน
    raw_data = get_weather_data()       # 1. ดึง
    clean_data = transform_data(raw_data) # 2. จัด
    load_to_bigquery(clean_data)        # 3. ส่ง