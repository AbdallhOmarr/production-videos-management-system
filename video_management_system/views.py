from django.shortcuts import render,redirect
from django.conf import settings
from .forms import VideoForm

import cv2
import os

from .tasks import process_video_task



# Create your views here.
def home(request):
    return render(request,"home.html")



def upload_videos(request):
    process_video_task.delay
    return render(request, "upload_video.html")


def upload_videos2(request):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            video_instance = form.save(commit=False)

            # Save the uploaded file to a temporary location
            video_file = request.FILES['video_file']
            temp_dir = os.path.join(settings.MEDIA_ROOT, 'temp')
            os.makedirs(temp_dir, exist_ok=True)
            file_path = os.path.join(temp_dir, video_file.name)
            
            with open(file_path, 'wb') as destination:
                for chunk in video_file.chunks():
                    destination.write(chunk)

            # Process the video asynchronously with Celery
            process_video_task.delay(file_path, request.POST)

            # Save the processed video to the model instance
            video_instance.video_file = video_file
            video_instance.save()


            return redirect('upload')  # Redirect to a success page

    return render(request, "upload_video.html")
