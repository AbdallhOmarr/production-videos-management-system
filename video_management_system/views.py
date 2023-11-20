from django.shortcuts import render,redirect
from django.conf import settings
from .forms import VideoForm

import cv2
import os


# Create your views here.
def home(request):
    return render(request,"home.html")

import re

def validate_filename(filename):
    # Define the regex pattern for valid filename characters
    pattern = r"^[a-zA-Z0-9_\-.]{1,255}$"

    # Check if the filename matches the pattern
    if re.match(pattern, filename):
        return True
    else:
        return False

def sanitize_filename(filename):
    invalid_chars = r"[^\w\.-]"

    # Replace invalid characters with underscores
    sanitized_filename = re.sub(invalid_chars, "_", filename)
    return sanitized_filename

def process_video(video_file,post_data):
    request_data = dict(post_data)
    # Define the temporary directory within MEDIA_ROOT
    temp_dir = os.path.join(settings.MEDIA_ROOT, 'temp')
    videos_dir=  os.path.join(settings.MEDIA_ROOT, 'videos')

    # Create the temporary directory if it doesn't exist
    os.makedirs(temp_dir, exist_ok=True)

    # Save the uploaded file to a temporary location
    file_path = os.path.join(temp_dir, video_file.name)
    
    with open(file_path, 'wb') as destination:
        for chunk in video_file.chunks():
            destination.write(chunk)

    # Now, use the file_path to read the video using OpenCV
    cap = cv2.VideoCapture(file_path)

    # Get the frames per second (fps) of the video
    fps = cap.get(cv2.CAP_PROP_FPS)

    # Define the codec and create a VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')    
    
    
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

    # Create the file_name by joining the valid values with "_"
    file_name = "_".join(valid_values)   
    file_name = file_name + ".mp4"  
    # Validate the filename
    # if validate_filename(file_name):
    #     # Sanitize the filename
    #     sanitized_filename = sanitize_filename(file_name)
    #     file_name = sanitized_filename + ".mp4"
    # else:
    #     # Handle invalid filename error
    #     print("Invalid filename provided")

    out_path = os.path.join(videos_dir, file_name)
    
    out = cv2.VideoWriter(out_path, fourcc, fps, (480, int(480 * cap.get(cv2.CAP_PROP_FRAME_HEIGHT) / cap.get(cv2.CAP_PROP_FRAME_WIDTH))))
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

    # Remove the temporary file after processing
    os.remove(file_path)

def upload_videos(request):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            video_instance = form.save(commit=False)
            
            # Process the video before saving
            video_file = request.FILES['video_file']
            process_video(video_file,request.POST)
            
            # Save the processed video to the model instance
            video_instance.video_file = video_file
            video_instance.save()

            # You can perform additional processing here before saving to the database

            return redirect('upload')  # Redirect to a success page

    return render(request, "upload_video.html")
