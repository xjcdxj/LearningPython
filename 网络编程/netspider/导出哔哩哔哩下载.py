import json
import os
import shutil
from concurrent.futures import ThreadPoolExecutor


def parse_video(old_path, new_path):
    shutil.copy(old_path, new_path)


def extract_video_task(item_path):
    with open(f'{item_path}/entry.json', 'r',encoding='utf-8') as f:
        video_information = json.load(f)
    folder_name = video_information['title']
    try:
        os.mkdir(f'{working_path}/{folder_name}')
    except FileExistsError:
        pass
    file_name = video_information['page_data']["part"]+'.mp4'
    video_folder = video_information['type_tag']
    print(file_name)
    for each in os.listdir(f'{item_path}/{video_folder}'):
        if each.endswith('blv'):
            parse_video(f'{item_path}/{video_folder}/{each}', f'{working_path}/{folder_name}/{file_name}')
    pass


def run():
    all_video_folders = os.listdir(cache_path)
    print(f'总共有{len(all_video_folders)}个视频')
    for each_path in all_video_folders:
        extract_video_task(f'{cache_path}/{each_path}')
        # thread_pool.submit(extract_video_task, f'{cache_path}/{each_path}')
    pass


if __name__ == '__main__':
    working_path = 'C:/Users/YuXjc/Desktop'
    cache_path = 'C:/Users/YuXjc/Desktop/9784617'
    THREAD_NUM = 10
    thread_pool = ThreadPoolExecutor(THREAD_NUM)
    run()
    pass
