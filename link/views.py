from googleapiclient.discovery import build
import pandas as pd
from django.shortcuts import render
from django.conf import settings
from .forms import VideoForm

def home(request):
    if request.method == 'POST':
        form = VideoForm(request.POST)
        if form.is_valid():
            video_url = form.cleaned_data['video_link']
            api_key = 'AIzaSyCq7Q0ELgdp9VjTcPyytE9dyWJg8rXEo5I'

            video_id = video_url.split("v=")[1].split("&")[0]

            youtube = build('youtube', 'v3', developerKey=api_key)

            response = youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                maxResults=1000,
                textFormat="plainText"  
            ).execute()

            comments = []
            for item in response['items']:
                comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
                comments.append(comment)

            d = {'comments': comments}
            df = pd.DataFrame(data=d)
            df.to_csv('media/comments.csv', index=False)
            return render(request, 'home.html', {'form': form, 'text': 'download'})
        
    else:
        form = VideoForm()

    return render(request, 'home.html', {'form': form})


import os
from django.http import HttpResponse

def download_file(request):
    file_path = os.path.join(settings.MEDIA_ROOT, 'comments.csv')
    with open(file_path, 'rb') as file:
        response = HttpResponse(file.read(), content_type="text/csv")
        response['Content-Disposition'] = f"attachment; filename=comments.csv"
        return response

