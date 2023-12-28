from django.shortcuts import render,redirect
from django.conf import settings
from .forms import VideoForm

import cv2
import os

from .tasks import process_video_task

from .models import Video
from django.db.models import Q
import re 

import pandas as pd 
import plotly.express as px
# Create your views here.
def home(request):
    return render(request,"home.html")




def upload_videos(request):
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

            video_instance.video_file = None
            video_instance.save()
            # Process the video asynchronously with Celery
            process_video_task.delay(file_path, request.POST,video_instance.id)


            return redirect('upload')  # Redirect to a success page

    return render(request, "upload_video.html")



def search_videos(request):
    
    if request.method == 'POST':

        search_param = request.POST.get('search-input')
        if search_param == "" :
            videos = Video.objects.all()
            for video_obj in videos:
                vid_path = video_obj.video_file.name
                split_vid_path = vid_path.split('\\')
                video_obj.video_file.name = split_vid_path[-1]
            print("splitted name")
            print(video_obj.video_file.name)        

            context = {
                'videos': videos,
            }
        else:
            search_keywords = re.findall(r'\b\w+(?:\s*\w*\d\s*)*\b', search_param)
            print(search_keywords)
            results = []

            for keyword in search_keywords:
                query = Q(product_code__contains=keyword) | Q(product_description__contains=keyword) | Q(factory__contains=keyword) | Q(operation_code__contains=keyword) | Q(machine_number__contains=keyword) | Q(machine_description__contains=keyword) | Q(operator_code__contains=keyword) | Q(operator_name__contains=keyword) | Q(additional_details__contains=keyword)
                
                # Convert the QuerySet to a list and extend the results list
                results.extend(list(Video.objects.filter(query)))

            # Use set to remove duplicates based on the object's ID
            unique_results = list(set(results))
            print("splitted name")

            print(unique_results)
            for video_obj in unique_results:
                vid_path = video_obj.video_file.name
                split_vid_path = vid_path.split('\\')
                video_obj.video_file.name = split_vid_path[-1]
                print(video_obj.video_file.name)        

            
            context = {
                'videos': unique_results,
            }


    else:
        videos = Video.objects.all()
        for video_obj in videos:
            vid_path = video_obj.video_file.name
            split_vid_path = vid_path.split('\\')
            video_obj.video_file.name = split_vid_path[-1]
            print("splitted name")
            print(video_obj.video_file.name)        
        context = {
            'videos': videos,
        }

    return render(request, 'search.html', context)


def about(request):
    return render(request,"about.html")



def plotly_chart_view(request):
    
    data_objects = Video.objects.all()
    data_list = list(data_objects.values())
    
    df = pd.DataFrame(data_list)

    #group by 
    grouped_df = df.groupby(by=['factory']).count()
    
    # Create a Plotly bar chart 
    fig = px.bar(grouped_df, x=grouped_df.index, y=grouped_df['video_file'], labels={'x': 'Factory', 'y': 'No. of videos'})
    # Update chart layout to add title and ylabel
    fig.update_layout(
        title='No. of videos by factory',
        yaxis=dict(title='No. of videos'),
        title_x = 0.5
    )
    plot_div = fig.to_html(full_html=False)


    # group by item
    no_of_unique_products = df['product_code'].nunique() #this number is 30 its int value
    
     # Create a Plotly bar chart 
    fig = px.bar(x=['Product Codes'], y=[no_of_unique_products], labels={'x': '', 'y': ''})
    
    # Update chart layout to add title and ylabel
    fig.update_layout(
        title='Count of Unique Product Codes',
        title_x = 0.5
    )
    plot_div2 = fig.to_html(full_html=False)


    #group by 
    grouped_df = df.groupby(by=['operation_code']).count()
    
    # Create a Plotly bar chart 
    fig = px.bar(grouped_df, x=grouped_df.index, y=grouped_df['video_file'], labels={'x': 'operation_code', 'y': 'No. of videos'})
    # Update chart layout to add title and ylabel
    fig.update_layout(
        title='No. of videos by operation code',
        yaxis=dict(title='No. of videos'),
        title_x = 0.5
    )
    plot_div3 = fig.to_html(full_html=False)

    
    return render(request, 'charts.html', {'plot_div': plot_div,'plot_div2': plot_div2,"plot_div3":plot_div3})