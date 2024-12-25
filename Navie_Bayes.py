import pandas as pd
import numpy as np

# Đọc dữ liệu từ file CSV
df = pd.read_csv('weather_data.csv')

# Tính xác suất tiên nghiệm cho từng loại thời tiết
weather_prior = df['Weather'].value_counts(normalize=True)

# Tính trung bình và độ lệch chuẩn cho từng đặc trưng theo từng loại thời tiết
weather_stats = df.groupby('Weather').agg(['mean', 'std'])

# Hàm tính xác suất Gaussian
def gaussian_probability(x, mean, std):
    if std == 0:  # Trường hợp độ lệch chuẩn bằng 0
        return 1.0 if x == mean else 0.0
    exponent = np.exp(-((x - mean) ** 2) / (2 * std ** 2))
    return (1 / (np.sqrt(2 * np.pi) * std)) * exponent

# Hàm dự báo thời tiết
def predict_weather(new_data):
    results = {}
    for weather in weather_prior.index:
        # Lấy trung bình và độ lệch chuẩn cho từng đặc trưng
        temp_mean, temp_std = weather_stats.loc[weather, ('Temperature', 'mean')], weather_stats.loc[weather, ('Temperature', 'std')]
        hum_mean, hum_std = weather_stats.loc[weather, ('Humidity', 'mean')], weather_stats.loc[weather, ('Humidity', 'std')]
        wind_mean, wind_std = weather_stats.loc[weather, ('WindSpeed', 'mean')], weather_stats.loc[weather, ('WindSpeed', 'std')]
        rain_mean, rain_std = weather_stats.loc[weather, ('Rainfall', 'mean')], weather_stats.loc[weather, ('Rainfall', 'std')]
        cloud_mean, cloud_std = weather_stats.loc[weather, ('Cloud Cover', 'mean')], weather_stats.loc[weather, ('Cloud Cover', 'std')]

        # Tính xác suất có điều kiện cho từng đặc trưng
        temp_prob = gaussian_probability(new_data['Temperature'], temp_mean, temp_std)
        hum_prob = gaussian_probability(new_data['Humidity'], hum_mean, hum_std)
        wind_prob = gaussian_probability(new_data['WindSpeed'], wind_mean, wind_std)
        rain_prob = gaussian_probability(new_data['Rainfall'], rain_mean, rain_std)
        cloud_prob = gaussian_probability(new_data['Cloud Cover'], cloud_mean, cloud_std)

        # Tính xác suất tổng hợp cho loại thời tiết hiện tại
        results[weather] = temp_prob * hum_prob * wind_prob * rain_prob * cloud_prob * weather_prior[weather]

    # Hiển thị các xác suất cho từng loại thời tiết
    for weather,probability, in results.items():
        print(f"{weather}: {probability:.50f}")

    # Chọn loại thời tiết có xác suất lớn nhất
    predicted_weather = max(results, key=results.get)
    return predicted_weather
print('DỰ BÁO THỜI TIẾT SỬ DỤNG NAVIE BAYES')
# Nhập dữ liệu mới để dự đoán
new_data = {
    'Temperature': float(input("Nhập nhiệt độ: ")),
    'Humidity': float(input("Nhập độ ẩm: ")),
    'WindSpeed': float(input("Nhập tốc độ gió: ")),
    'Rainfall': float(input("Nhập lượng mưa: ")),
    'Cloud Cover': float(input("Nhập độ bao phủ mây: "))
}
print('-------------------------------')
print('Xác xuất cho từng loại thời tiết')

# Dự đoán thời tiết

predicted_weather = predict_weather(new_data)
print('-------------------------------')
print("Dự Báo Thời Tiết:", predicted_weather)
