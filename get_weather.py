# 1. เรียกใช้เครื่องมือ requests ที่เราเพิ่งติดตั้ง
import requests 
# เรียกใช้ json เพื่อช่วยจัดหน้าตาข้อมูลให้อ่านง่าย
import json 

# 2. ใส่กุญแจและเป้าหมายของเรา
# เอา Key ที่ Copy ไว้ในก้าวที่ 1 มาใส่ตรงนี้ (อย่าลืมใส่เครื่องหมายคำพูด "" ครอบด้วยนะ)
API_KEY = "3e239c0e823ec74c848a709eec04db19" 

# เมืองที่เราอยากรู้ (ลองเปลี่ยนเป็น Chiang Mai หรือ Phuket ก็ได้)
CITY_NAME = "Bangkok" 

# 3. สร้าง URL (ลิงก์) สำหรับขอข้อมูล
# นี่คือรูปแบบที่ OpenWeatherMap กำหนดมา เราแค่เอาตัวแปรไปแทรก
url = f"https://api.openweathermap.org/data/2.5/weather?q={CITY_NAME}&appid={API_KEY}&units=metric"

# 4. สั่งให้ requests วิ่งไปที่ URL นั้นเพื่อขอข้อมูล (GET)
print(f"กำลังขอข้อมูลสภาพอากาศของ {CITY_NAME}...")
response = requests.get(url)

# 5. เช็คว่าคุยกันรู้เรื่องไหม?
# 200 แปลว่า OK (สำเร็จ), 404 แปลว่า ไม่เจอ (ชื่อเมืองผิด), 401 แปลว่า Key ผิด
if response.status_code == 200:
    print("✅ สำเร็จ! ได้ข้อมูลมาแล้ว")
    
    # 6. แปลงข้อมูลที่ได้ (JSON) มาเป็นสิ่งที่ Python เข้าใจ (Dictionary)
    data = response.json()
    
    # ลองปริ้นท์ดูข้อมูลดิบๆ ทั้งหมดก่อน (ใช้ json.dumps จัดให้อ่านง่ายขึ้น)
    print("--- ข้อมูลดิบ (JSON) ---")
    print(json.dumps(data, indent=4, ensure_ascii=False))
    
    # 7. เจาะเอาเฉพาะข้อมูลที่เราสนใจ
    # สังเกตโครงสร้าง JSON: อุณหภูมิจะซ่อนอยู่ในกล่องชื่อ 'main'
    temp = data['main']['temp'] 
    humidity = data['main']['humidity']
    # สภาพอากาศ (เช่น เมฆมาก, ฝนตก) อยู่ในกล่อง 'weather' ตัวแรก [0]
    description = data['weather'][0]['description']
    
    print("--- สรุปผล ---")
    print(f"อุณหภูมิ: {temp} องศาเซลเซียส")
    print(f"ความชื้น: {humidity}%")
    print(f"สภาพอากาศ: {description}")

else:
    # ถ้าไม่สำเร็จ ให้บอกหน่อยว่าเพราะอะไร
    print("❌ เกิดข้อผิดพลาด!")
    print(f"รหัสความผิดพลาด: {response.status_code}")
    print(f"ข้อความจาก Server: {response.text}")
