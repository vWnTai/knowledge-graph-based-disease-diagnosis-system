import pandas as pd

# 1. Khai báo tên file Excel của bạn (Nhớ đổi tên cho đúng file thực tế)
file_excel = 'DM ICD10-19_8_BYT.xlsx' 

print("--- Đang quét cấu trúc file Excel... ---")

# 2. Đọc thử 15 dòng đầu tiên dưới dạng thô (không lấy header) để dò tìm
df_raw = pd.read_excel(file_excel, header=None, nrows=15)

header_idx = None
# Duyệt qua từng dòng để tìm dòng chứa chữ "Mã" hoặc "STT"
for idx, row in df_raw.iterrows():
    row_str = row.astype(str).str.strip().tolist()
    if 'Mã' in row_str or 'STT' in row_str:
        header_idx = idx
        break

# 3. Xử lý dựa trên kết quả dò tìm
if header_idx is not None:
    print(f" Tìm thấy dòng tiêu đề thực sự ở dòng số: {header_idx} (tính từ 0)")
    # Đọc lại file với chính xác dòng header vừa tìm được
    df = pd.read_excel(file_excel, header=header_idx)
else:
    print("❌ LỖI: Đã quét 15 dòng đầu nhưng không thấy chữ 'Mã' hay 'STT' ở đâu.")
    print("Dưới đây là 5 dòng đầu tiên của file, bạn xem thử nó đang chứa gì nhé:")
    print(df_raw.head(5))
    exit()

# 4. Làm sạch tên cột (Xóa khoảng trắng thừa nếu có)
df.columns = df.columns.str.strip()

# 5. Nhập từ khóa cần lọc
user_input = input("\nNhập mã cần quét (Ví dụ: Z): ").strip()

# Ép cột 'Mã' về kiểu chuỗi và xóa khoảng trắng để tránh lỗi dữ liệu
df['Mã'] = df['Mã'].astype(str).str.strip()

# Lọc các dòng có mã bắt đầu bằng ký tự user nhập
filtered_df = df[df['Mã'].str.startswith(user_input, na=False)]

# 6. Xuất kết quả ra CSV
if not filtered_df.empty:
    output_file = f"ket_qua_loc_{user_input}.csv"
    # Lấy ra 2 cột Mã và Tên bệnh (hoặc lấy tất cả các cột bằng cách bỏ [['Mã', 'Tên bệnh']])
    filtered_df[['Mã', 'Tên bệnh']].to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f" Đã xuất file thành công: {output_file}")
else:
    print(f" Không tìm thấy mã nào bắt đầu bằng ký tự: {user_input}")