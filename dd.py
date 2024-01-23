import instaloader
import os
import pickle
import time
import requests
import qrcode
import random

def download_posts_data(instagram_data_path, posts_per_account, pickle_directory, media_directory):
    try:
        L = instaloader.Instaloader()

        # Замените 'your_instagram_username' и 'your_instagram_password' на ваши реальные учетные данные
        username = 'gggg_gkkkkllll'
        password = '777kaz777'

        # Установка User-Agent
        L.context.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0"}

        # Вход в аккаунт Instagram
        L.context.debug = True  # Включаем вывод отладочной информации

        L.login(username, password)

        with open(instagram_data_path, 'rb') as instagram_data_file:
            instagram_data = pickle.load(instagram_data_file)

        accounts_data = []

        for data in instagram_data:
            account_name = data.get('account_name')
            school_id = data.get('school')
    
            if account_name is None or not account_name:
                print("Error: 'account_name' key is missing or empty in account data. Skipping.")
                continue

            print(f"Processing account {account_name} from school {school_id}")

            try:
                profile = instaloader.Profile.from_username(L.context, account_name)
            except instaloader.exceptions.ProfileNotExistsException:
                print(f"Profile {account_name} does not exist.")
                continue

            account_data = []

            count = 0
            for post in profile.get_posts():
                if count >= posts_per_account:
                    break
            
                post_id = str(post.mediaid)

                # Проверка, был ли этот пост загружен ранее
                if any(entry['id'] == post_id for entry in accounts_data):
                    print(f"Post {post_id} already downloaded. Skipping.")
                    continue

                post_data = {
                    'id': str(post.mediaid),
                    'text': post.caption,
                    'timestamp': post.date_utc.timestamp(),
                    'media': [],
                    'qr_code': '',  # Создаем пустую строку для qr_code
                    'login': account_name,
                    'school': school_id
                }

                try:
                    # Проверяем, есть ли видео в карусели или сам пост является видео
                    if post.is_video:
                        print('video')
                        # Если у поста видео
                        media_data = {}  # Создаем структуру данных для видео
                        
                        # Увеличьте время ожидания перед запросом к видео
                        time.sleep(random.uniform(10, 15))
                        
                        video_url = f"https://www.instagram.com/p/{post.shortcode}/"
                        qr_code_path = os.path.join(media_directory, f"{post.mediaid}_video_qr.png")

                        # Генерация QR-кода для видео
                        qr = qrcode.QRCode(
                            version=1,
                            error_correction=qrcode.constants.ERROR_CORRECT_L,
                            box_size=10,
                            border=4,
                        )
                        qr.add_data(video_url)
                        qr.make(fit=True)

                        img = qr.make_image(fill_color="black", back_color="white")
                        img.save(qr_code_path)
                        print(f"Generated QR code for video: {qr_code_path}")

                        post_data['qr_code'] = qr_code_path  # Обновляем qr_code для всего поста
                        post_data['media'].append(media_data)

                    elif post.typename == 'GraphSidecar':
                        print('karusel')
                        # Если у поста карусель изображений
                        for index, node in enumerate(post.get_sidecar_nodes()):
                            media_data = {}  # Создаем структуру данных для медиа

                            # Добавьте дополнительное время ожидания перед запросом к элементу карусели
                            time.sleep(random.uniform(3, 6))

                            if node.is_video:
                                # Если у элемента карусели видео, добавим QR-код для видео в карусели
                                video_url = f"https://www.instagram.com/p/{post.shortcode}/"
                                qr_code_path = os.path.join(media_directory, f"{post.mediaid}_video_qr.png")

                                # Генерация QR-кода для видео
                                qr = qrcode.QRCode(
                                    version=1,
                                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                                    box_size=10,
                                    border=4,
                                )
                                qr.add_data(video_url)
                                qr.make(fit=True)

                                img = qr.make_image(fill_color="black", back_color="white")
                                img.save(qr_code_path)
                                print(f"Generated QR code for video: {qr_code_path}")

                                post_data['qr_code'] = qr_code_path  # Обновляем qr_code для всего поста
                                post_data['media'].append(media_data) # Обновляем qr_code для текущего элемента карусели
                            else:
                                # Если у элемента карусели изображение
                                time.sleep(random.uniform(3, 6))

                                media_data[f'post_photos_{index + 1}'] = os.path.join(media_directory, f"{post.mediaid}_{index}.jpg")
                                with open(media_data[f'post_photos_{index + 1}'], 'wb') as media_file:
                                    media_file.write(requests.get(node.display_url).content)
                                post_data['media'].append(media_data)
                                print(f"Downloaded media for post {post.mediaid}: {media_data}")

                    else:
                        print('foto')
                        # Если у поста только одно изображение
                        media_data = {}  # Создаем структуру данных для медиа
                        time.sleep(random.uniform(3, 6))

                        media_data[f'post_photos_1'] = os.path.join(media_directory, f"{post.mediaid}_1.jpg")
                        with open(media_data[f'post_photos_1'], 'wb') as media_file:
                            media_file.write(requests.get(post.url).content)
                        post_data['media'].append(media_data)
                        print(f"Downloaded media for post {post.mediaid}: {media_data}")

                    account_data.append(post_data)
                    count += 1
                    time.sleep(random.uniform(3, 6))  # Добавим случайную задержку от 3 до 6 секунд для эмуляции человеческого поведения

                except Exception as e:
                    print(f"Failed to fetch metadata for post {post.mediaid}. Error: {e}")

            accounts_data.extend(account_data)

        instagram_pickle_path = os.path.join(pickle_directory, 'instagram_data.pickle')
        with open(instagram_pickle_path, 'wb') as instagram_pickle_file:
            pickle.dump(accounts_data, instagram_pickle_file)

        print(f"Данные Instagram успешно сохранены в pickle файл: {instagram_pickle_path}")

    except instaloader.exceptions.InstaloaderException as e:
        print("Ошибка при загрузке данных:", e)

if __name__ == "__main__":
    instagram_data_path = 'C:/Users/Professional/Desktop/instapars/instapars/school_socialmedia_data.pickle'
    posts_per_account = 1
    pickle_directory = 'C:/Users/Professional/Desktop/instapars/instapars'
    media_directory = 'C:/Users/Professional/Desktop/instapars/instapars/media'

    download_posts_data(instagram_data_path, posts_per_account, pickle_directory, media_directory)
