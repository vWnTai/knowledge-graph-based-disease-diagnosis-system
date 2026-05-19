import requests
import pandas as pd
import time

# Danh sách các nhóm bệnh phổ biến (Section IDs) để demo cho đề tài
# Bạn có thể bổ sung thêm các mã nhóm khác từ file 22 chương trước vào đây
target_sections = [
    "A00-A09", "A15-A19", "B20-B24", # Nhóm nhiễm trùng
    "J00-J06", "J09-J18", "J20-J22", # Nhóm hô hấp
    "K20-K31", "K35-K38",            # Nhóm tiêu hóa
    "I10-I15", "I20-I25"             # Nhóm tuần hoàn
]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Origin": "https://icd.kcb.vn/icd-10/icd10", # Giả lập gọi từ trang gốc của họ
}

all_records = []

print("🚀 Bắt đầu quét dữ liệu chi tiết từ API White Neuron...")

for section_id in target_sections:
    # Ghép mã nhóm vào URL API bạn vừa tìm được
    api_url = f"https://ccs.whiteneuron.com/api/ICD10/data/section?id={section_id}&lang=vi"
    
    print(f"🔄 Đang gọi API nhóm: {section_id}...")
    
    try:
        response = requests.get(api_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            json_data = response.json()
            
            # Cấu trúc JSON chuẩn dựa theo ảnh bạn gửi trước đó
            if json_data.get("status") == "success" or "data" in json_data:
                items = json_data.get("data", [])
                
                for item in items:
                    inner_data = item.get("data", {})
                    
                    all_records.append({
                        "Nhóm gốc (Section)": section_id,
                        "Mã bệnh chi tiết": item.get("id"),       # Ví dụ: A00.0
                        "Tên bệnh tiếng Việt": inner_data.get("name"), # Chữ tiếng Việt chuẩn
                        "Cấp độ": item.get("model"),               # Thường là 'code' hoặc 'sub-code'
                        "Là cấp cuối (Leaf)": item.get("is_leaf")  # True có nghĩa là mã bệnh gốc kịch trần
                    })
            else:
                print(f"⚠️ API trả về cấu trúc lạ hoặc không thành công tại nhóm {section_id}")
        else:
            print(f"❌ Lỗi HTTP {response.status_code} tại nhóm {section_id}")
            
        # Nghỉ 1 giây giữa các lần gọi để làm một Crawler lịch sự, không phá hoại hệ thống của họ
        time.sleep(1)
        
    except Exception as e:
        print(f"❌ Gặp lỗi kết nối tại nhóm {section_id}: {e}")

# Xuất kết quả ra file dữ liệu lớn cho NCKH
if all_records:
    df = pd.DataFrame(all_records)
    # Dùng utf-8-sig để lưu file tiếng Việt không bị lỗi font khi mở bằng Excel
    df.to_csv("danh_muc_benh_chi_tiet_byt.csv", index=False, encoding="utf-8-sig")
    
    print("\n🎉 XONG RỒI!")
    print(f"📊 Tổng cộng thu thập được: {len(df)} mã bệnh chi tiết chuẩn Bộ Y Tế.")
    print("💾 Đã lưu thành công vào file: 'danh_muc_benh_chi_tiet_byt.csv'")
else:
    print("❌ Không thu thập được dữ liệu nào, hãy kiểm tra lại kết nối mạng hoặc URL.")