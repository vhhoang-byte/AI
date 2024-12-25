import pandas as pd
import numpy as np

# Tạo dữ liệu giả lập
num_records = 100  # Số lượng bản ghi
data = {
    'ID': range(1, num_records + 1),
    'Temperature': np.random.randint(low= -10,high= 40,size= num_records),  # Nhiệt độ từ 0 đến 40°C
    'Humidity': np.random.randint(low=20,high= 100,size= num_records),   # Độ ẩm từ 20% đến 100%
    'WindSpeed': np.random.randint(low=0,high= 30, size=num_records),    # Tốc độ gió từ 0 đến 30 km/h
    'Rainfall': np.random.randint(low=0, high=101, size=num_records),    # Lượng mưa từ 0 đến 100 mm
    'Cloud Cover': np.random.randint(low=0,high= 101, size=num_records),  # Độ bao phủ mây từ 0% đến 100%
}

# Xác định nhãn thời tiết dựa trên các quy tắc giả định
def determine_weather(row):
    if row['Rainfall'] > 50:
        return 'Rainy'
    elif row['Temperature'] < 0:
        return 'Snowy'
    elif row['Cloud Cover'] > 70:
        return 'Cloudy'
    else:
        return 'Sunny'

# Tạo DataFrame và áp dụng quy tắc dự báo thời tiết
df = pd.DataFrame(data)
df['Weather'] = df.apply(determine_weather, axis=1)

# Lưu file CSV
df.to_csv('weather_data.csv', index=False)
print("Đã tạo file 'weather_data.csv' với các cột yêu cầu.")
