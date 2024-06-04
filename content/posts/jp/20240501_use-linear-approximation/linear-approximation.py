import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
from datetime import datetime

# データの準備
x_data = [202105, 202107, 202109, 202111, 202201, 202203, 202205, 202207, 202209, 202211, 202301, 202303, 202305, 202307, 202309, 202311, 202401, 202403, 202405]
x = np.array([datetime.strptime(str(date), '%Y%m').timestamp() for date in x_data])
y = np.array([72, 73, 74, 75, 76, 78, 79, 80, 81, 82, 82, 83, 84, 85, 85, 86, 87, 87, 88])

model = LinearRegression()
model.fit(x[:, np.newaxis], y)

# 予測
x_new_data = [202407, 202409, 202411, 202501]
x_new = np.array([datetime.strptime(str(date), '%Y%m').timestamp() for date in x_new_data])
y_new = model.predict(x_new[:, np.newaxis])
print(y_new)

# 散布図と線形回帰結果の可視化
plt.figure(figsize=(10, 6))

# 散布図
x_dates = [datetime.strptime(str(date), '%Y%m') for date in x_data]
plt.scatter(x_dates, y, color='blue', label='real data')

# 線形回帰の直線
plt.plot(x_dates, model.predict(x[:, np.newaxis]), color='green', linestyle='-', label='regression line')

# 予測値
x_new_dates = [datetime.strptime(str(date), '%Y%m') for date in x_new_data]
plt.plot(x_new_dates, y_new, 'ro', label='Predicted value')

plt.yticks(range(68, 99, 2))
plt.xlim(x_dates[0], x_new_dates[-1])
plt.xlabel('year-month')
plt.ylabel('Average sales price per square meter of Ariake apartments in Koto Ward')
plt.title('Prediction by linear regression')
plt.legend()
plt.grid(True)
plt.tight_layout()

# 散布図保存
output_path = 'scatter_plot_with_regression.png'
plt.savefig(output_path)