import instaloader
import os
import pickle
import time

def download_posts_data(account_list, posts_per_account, pickle_directory):
    try:
        loader = instaloader.Instaloader()
        for account in account_list:
            loader.context.username = 'gggg_gkkkkllll'

            profile = instaloader.Profile.from_username(loader.context, account)
            count = 0

            existing_posts_data_file_path = os.path.join(pickle_directory, f'{account}_posts_data.pickle')
            if os.path.exists(existing_posts_data_file_path):
                with open(existing_posts_data_file_path, 'rb') as existing_posts_data_file:
                    existing_posts_data = pickle.load(existing_posts_data_file)
            else:
                existing_posts_data = []

            account_data = []

            for post in profile.get_posts():
                if count >= posts_per_account:
                    break

                if any(existing_post['id'] == str(post.mediaid) for existing_post in existing_posts_data):
                    print(f"Post {post.mediaid} already exists in the previous data. Skipping...")
                    continue

                post_data = {
                    'id': str(post.mediaid),
                    'text': post.caption,
                    'timestamp': post.date_utc.timestamp(),
                    'media': []  
                }

                for image in post.get_sidecar_nodes():
                    media_data = {
                        'url': image.display_url,
                        'is_video': image.is_video
                    }
                    post_data['media'].append(media_data)

                if post.is_video:
                    video_url = post.video_url
                    video_data = {
                        'url': video_url,
                        'is_video': True
                    }
                    post_data['media'].append(video_data)

                account_data.append(post_data)

                print(f"Downloaded data for post {count + 1} from {account}")
                print("-" * 30)

                count += 1

                time.sleep(2)

            pickle_file_path = os.path.join(pickle_directory, f'{account}_posts_data.pickle')
            with open(pickle_file_path, 'wb') as pickle_out:
                pickle.dump(account_data + existing_posts_data, pickle_out)

    except instaloader.exceptions.InstaloaderException as e:
        print("Ошибка:", e)


account_list = ['aya_shalkar']  
posts_per_account = 3  
pickle_directory = 'C:/Users/Professional/Desktop/instapars'

download_posts_data(account_list, posts_per_account, pickle_directory)
