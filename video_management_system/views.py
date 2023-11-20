from django.shortcuts import render,redirect
from django.conf import settings
from .forms import VideoForm

import cv2
import os


# Create your views here.
def home(request):
    return render(request,"home.html")


def process_video(video_file,request_data):
    print()
    # Define the temporary directory within MEDIA_ROOT
    temp_dir = os.path.join(settings.MEDIA_ROOT, 'temp')

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
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    
    file_name = request_data['product_code'] + "_"  + request_data['product_description'] + "_" + request_data['factory'] + "_" + request_data['operation_code'] + "_" + request_data['operation_description'] + "_" + request_data['machine_number'] + "_" + request_data['machine_description'] 
    out_path = os.path.splitext(file_path)[0] + '_resized.avi'
    
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
