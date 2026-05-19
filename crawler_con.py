import requests
import pandas as pd
import time

# 1. Đọc lại file 22 chương gốc bạn vừa lưu được
df_chapters = pd.read_csv("icd10_cac_chuong_goc.csv")

# 2. Cấu hình URL con (Hãy đổi lại theo đúng link bạn bắt được ở tab Network khi click vào Chương)
# Ví dụ mẫu: "https://api.icd-vietnam.com/api/icd10/child?parent="
BASE_CHILD_URL = "https://ccs.whiteneuron.com/api/ICD10/data/section?id=A00-A09&lang=vi" 

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

all_diseases = []

# 3. Vòng lặp tự động duyệt qua 22 chương
for index, row in df_chapters.iterrows():
    chapter_id = row["Mã khoảng bệnh"]
    chapter_name = row["Tên chương tiếng Việt"]
    
    # Tạo URL động cho từng chương (ví dụ: .../child?parent=A00-B99)
    child_url = f"{BASE_CHILD_URL}{chapter_id}" 
    
    print(f"🔄 Đang quét danh mục con của: {chapter_name} ({chapter_id})...")
    
    try:
        response = requests.get(child_url, headers=headers)
        if response.status_code == 200:
            json_data = response.json()
            items = json_data.get("data", [])
            
            for item in items:
                inner_data = item.get("data", {})
                all_diseases.append({
                    "Chương gốc": chapter_name,
                    "Mã cấp con": item.get("id"), # Ví dụ: A00-A09 hoặc A00
                    "Tên bệnh/Nhóm bệnh": inner_data.get("name"),
                    "Là cấp cuối chưa": item.get("is_leaf") # Nếu True tức là đã chạm đáy mã bệnh
                })
        else:
            print(f"❌ Lỗi khi quét mã {chapter_id}, HTTP code: {response.status_code}")
            
        # 💡 Mẹo xương máu NCKH: Nghỉ 1 giây sau mỗi chương để tránh bị hệ thống block IP
        time.sleep(1) 
        
    except Exception as e:
        print(f"❌ Gặp lỗi tại chương {chapter_id}: {e}")

# 4. Xuất toàn bộ kho dữ liệu đa tầng ra file CSV
if all_diseases:
    df_result = pd.DataFrame(all_diseases)
    df_result.to_csv("icd10_data_toan_tap.csv", index=False, encoding="utf-8-sig")
    print(f"\n🎉 THÀNH CÔNG RỰC RỠ! Đã thu thập được tổng cộng {len(df_result)} mục bệnh lý.")
    print("💾 Dữ liệu đã được đóng gói an toàn tại file 'icd10_data_toan_tap.csv'")