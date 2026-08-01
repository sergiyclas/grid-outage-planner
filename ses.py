import matplotlib.pyplot as plt
import numpy as np

# Години доби
hours = list(range(24))

# Вироблення електроенергії в залежності від години
# Припустимо, що максимальна потужність станції досягається в обідній час (12:00)
# Для спрощення візьмемо вигляд гауссової кривої



# Генерація гауссової кривої для симуляції добового циклу
def generate_daily_output(hours, peak_power=1.0):
    # Параметри гауссової кривої
    mean = 12  # Година піку (середина дня)
    std_dev = 3  # Стандартне відхилення
    peak = peak_power
    output = peak * np.exp(-0.5 * ((np.array(hours) - mean) / std_dev) ** 2)
    print(output)
    return output

# Обчислення вироблення
production = generate_daily_output(hours)

# Побудова графіку
plt.figure(figsize=(10, 6))
plt.plot(hours, production, label='Вироблення електроенергії', color='orange')
plt.xlabel('Години доби')
plt.ylabel('Вироблення електроенергії (кіловат-години)')
plt.title('Вироблення електроенергії домашньої сонячної станції протягом доби')
plt.grid(True)
plt.legend()
plt.xticks(hours)
plt.tight_layout()
plt.show()

