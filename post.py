import pickle
import json

# Путь к файлу pickle
pickle_file_path = 'C:/Users/dg078/Desktop/instaloader/instagram_data.pickle'

# Путь для сохранения JSON-файла
json_file_path = 'C:/Users/dg078/Desktop/instaloader/instagram_data.json'

# Открываем pickle файл и загружаем данные
with open(pickle_file_path, 'rb') as pickle_file:
    instagram_data = pickle.load(pickle_file)

# Записываем данные в JSON-файл
with open(json_file_path, 'w', encoding='utf-8') as json_file:
    json.dump(instagram_data, json_file, ensure_ascii=False, indent=4)

print(f"Данные успешно записаны в JSON-файл: {json_file_path}")
