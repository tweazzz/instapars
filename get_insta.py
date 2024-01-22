import os
import requests
import pickle

def save_school_socialmedia_data(school_socialmedia_data, pickle_directory):
    try:
        instagram_data = [data for data in school_socialmedia_data if data.get('type') == 'instagram']

        print("Instagram Data Before Saving:")
        print(instagram_data)

        pickle_file_path = os.path.join(pickle_directory, 'school_socialmedia_data.pickle')
        with open(pickle_file_path, 'wb') as pickle_file:
            pickle.dump(instagram_data, pickle_file)

        print(f"Данные о школах и аккаунтах Instagram успешно сохранены в {pickle_file_path}")

    except Exception as e:
        print("Ошибка при сохранении данных:", e)

def fetch_instagram_data(api_url, pickle_directory):
    try:
        response = requests.get(api_url)
        socialmedia_data = response.json()

        if response.status_code != 200:
            print(f"Ошибка при запросе данных: {response.status_code}")
            return

        save_school_socialmedia_data(socialmedia_data, pickle_directory)

    except Exception as e:
        print("Ошибка при запросе данных:", e)

if __name__ == "__main__":
    api_url = 'https://www.bilimge.kz/admins/api/School_SocialMediaApi/'
    pickle_directory = 'C:/Users/dg078/Desktop/instaloader'

    fetch_instagram_data(api_url, pickle_directory)