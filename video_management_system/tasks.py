
from celery import shared_task
from django.conf import settings
import os
import cv2
import logging
from base.celery import app
from .models import Video
from datetime import datetime
import os
import re

from datetime import datetime 

logger = logging.getLogger(__name__)

def get_creation_date(file_path):
    date_str = datetime.fromtimestamp(os.path.getctime(file_path))
    formatted_date =  date_str.strftime("%Y-%m-%d_%H-%M-%S")
    return formatted_date

def clean_file_name(filename):
        # Check for invalid characters in filename
    invalid_characters = re.compile(r'[\\/?*<>:"|]')
    if invalid_characters.search(filename):
        logger.error("Filename '{}' contains invalid characters".format(filename))

    # Sanitize filename by removing invalid characters
    cleaned_filename = re.sub(invalid_characters, '', filename)
    logger.info(f"Filename cleaned '{cleaned_filename}'")

    return cleaned_filename    

## tasks 
@app.task
def process_video_task(file_path, post_data,video_id):
    try:
        logger.info("Task started")
        request_data = dict(post_data)
        # Define the directory within MEDIA_ROOT
        # videos_dir=  os.path.join(settings.MEDIA_ROOT, 'videos')
        videos_dir = r"\\Qnap02\Process\VIDEOS\VIDEOS\web_interface"
        # Create the temporary directory if it doesn't exist
        os.makedirs(videos_dir, exist_ok=True)

        # Now, use the file_path to read the video using OpenCV
        cap = cv2.VideoCapture(file_path)

        # Get the frames per second (fps) of the video
        fps = cap.get(cv2.CAP_PROP_FPS)

        # Define the codec and create a VideoWriter object
        fourcc = cv2.VideoWriter_fourcc(*'avc1')    
        # # codecs
        # XVID
        # avc1
        
        # List of keys you want to remove
        keys_to_remove = ['csrfmiddlewaretoken']

        # Remove the specified keys from the QueryDict
        for key in keys_to_remove:
            request_data.pop(key, None)

        # Initialize an empty list to store non-empty values
        valid_values = []
        
        # Loop through the values and filter out empty, None, or ""
        for value in request_data.values():
            if value is not None and value != "":
                if type(value) == type([]):
                    value = value[0]
                valid_values.append(value)

        video_creation_date = get_creation_date(file_path)
        logger.info(f"Video creation date: {video_creation_date}")
        valid_values.append(video_creation_date)
        
        # Create the file_name by joining the valid values with "_"
        file_name = "_".join(valid_values)   
        file_name = file_name + ".mp4"  
        # Validate the filename
        file_name = clean_file_name(file_name)
        
        
        out_path = os.path.join(videos_dir, file_name)
        logger.info(f"Video out path:{out_path}")

        out = cv2.VideoWriter(out_path, fourcc, fps, (640, int(640 * cap.get(cv2.CAP_PROP_FRAME_HEIGHT) / cap.get(cv2.CAP_PROP_FRAME_WIDTH))))
        # Read and resize each frame
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            resized_frame = cv2.resize(frame, (640, int(640 * frame.shape[0] / frame.shape[1])))
            out.write(resized_frame)

        # Release video capture and writer objects
        cap.release()
        out.release()
        # You can perform additional processing here before saving to the database

        video_instance = Video.objects.get(id=video_id)
        video_instance.video_file = out_path
        video_instance.save()
        

    except Exception as e :
        logger.error(f"Error processing video: {str(e)}")
        # delete the video obj from database 
        video_instance = Video.objects.get(id=video_id)
        video_instance.delete()
        raise e
    
    finally:
        
        try:
            os.remove(file_path)
        except:
            logger.info("processing completed but temp failed to delete")
        logger.info("Task Completed")