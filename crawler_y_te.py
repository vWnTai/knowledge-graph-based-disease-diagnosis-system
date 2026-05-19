import requests
import pandas as pd

# BƯỚC 1: Hãy dán cái Request URL đầy đủ bạn copy từ tab Headers vào đây
URL = "https://ccs.whiteneuron.com/api/ICD10/root?lang=vi"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

print("🚀 Đang kết nối thẳng vào API của hệ thống...")
response = requests.get(URL, headers=headers)

if response.status_code == 200:
    # Python tự động giải mã \u1ec7 thành chữ "ệ" tiếng Việt chuẩn
    json_data = response.json() 
    
    if json_data.get("status") == "success":
        raw_items = json_data.get("data", [])
        cleaned_list = []
        
        for item in raw_items:
            inner_data = item.get("data", {})
            cleaned_list.append({
                "Loại cấp độ": item.get("model"),          # Ví dụ: chapter
                "Mã khoảng bệnh": item.get("id"),         # Ví dụ: A00-B99
                "Đã là cấp cuối chưa": item.get("is_leaf"), # False = Còn cấp con bên trong
                "Mã số chương": inner_data.get("code"),     # Ví dụ: I, II, III
                "Tên chương tiếng Việt": inner_data.get("name") # Tên tiếng Việt sạch sẽ
            })
            
        # Chuyển thành bảng dữ liệu và xuất file
        df = pd.DataFrame(cleaned_list)
        df.to_csv("icd10_cac_chuong_goc.csv", index=False, encoding="utf-8-sig")
        
        print(f"🎉 Thành công! Đã quét được {len(cleaned_list)} Chương gốc của Bộ Y Tế.")
        print("💾 File đã lưu: 'icd10_cac_chuong_goc.csv'")
        
    else:
        print("❌ API trả về trạng thái không thành công.")
else:
    print(f"❌ Không thể gọi tới API. Mã lỗi hệ thống: {response.status_code}")