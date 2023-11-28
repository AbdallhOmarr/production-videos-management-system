import os
import imageio
from datetime import datetime

def get_media_creation_date(file_path):
    try:
        with imageio.get_reader(file_path) as reader:
            meta_data = reader.get_meta_data()
            print(meta_data)
            if 'creation_time' in meta_data:
                creation_time_str = meta_data['creation_time']
                media_creation_date = datetime.strptime(creation_time_str, "%Y-%m-%d %H:%M:%S")
                return media_creation_date
            else:
                print("error")
                return None
    except Exception as e:
        print(f"Error reading video metadata: {e}")
        return None
    
    

f = r'media\temp\2023-09-20 11-34-27.mkv'
get_media_creation_date(f)