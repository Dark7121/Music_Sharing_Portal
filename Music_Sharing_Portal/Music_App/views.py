from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, LoginForm, SongUploadForm, ProtectedSongForm
from .models import Song, User, ProtectedPlayList, ShareRequest, PrivatePlayList
from django.db.models import Q
import os
from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
import shutil

def home(request):
    return render(request, 'home.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            password1 = form.cleaned_data.get('password1')
            password2 = form.cleaned_data.get('password2')
            if password1 == password2:
                user = form.save()
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, "Passwords do not match.")
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def song_upload(request):
    if request.method == 'POST':
        form = SongUploadForm(request.POST, request.FILES)
        if form.is_valid():
            song = form.save(commit=False)
            song.uploaded_by = request.user
            song.save()
            return redirect('home')
    else:
        form = SongUploadForm()
    return render(request, 'song_upload.html', {'form': form})

@login_required
def search(request):
    query = request.GET.get('q')
    if query:
        songs = Song.objects.filter(Q(name__icontains=query) | Q(artist__icontains=query))
        if not songs:
            messages.info(request, "Sorry, the song you are searching is not uploaded by any user yet! You can go and upload it right now.")
    else:
        songs = Song.objects.all()
    return render(request, 'search.html', {'songs': songs, 'query': query})

@login_required
def song_list(request):
    songs = Song.objects.all()
    return render(request, 'song_list.html', {'songs': songs})

@login_required
def private_playlist(request):
    username = request.user.username
    private_playlist_dir = os.path.join(settings.PRIVATE_PLAYLIST_ROOT, username)
    songs = Song.objects.filter(uploaded_by=request.user)
    print(private_playlist_dir)
    print(songs)

    return render(request, 'private_playlist.html', {'songs': songs, 'private_playlist_dir': private_playlist_dir})



@login_required
def delete_song(request, song_id):
    song = Song.objects.get(id=song_id)
    
    os.remove(os.path.join(settings.MEDIA_ROOT, str(song.mp3_file)))
    os.remove(os.path.join(settings.MEDIA_ROOT, str(song.cover_image)))
    
    song.delete()
    return redirect ('home')

@login_required
def private_song_upload(request):
    if request.method == 'POST':
        form = SongUploadForm(request.POST, request.FILES)
        if form.is_valid():
            song = form.save(commit=False)
            song.uploaded_by = request.user
            song.save()
            
           
            private_playlist_dir = os.path.join(settings.PRIVATE_PLAYLIST_ROOT, request.user.username)
            if not os.path.exists(private_playlist_dir):
                os.makedirs(private_playlist_dir)

            
            mp3_file_path = os.path.join(settings.MEDIA_ROOT, str(song.mp3_file))
            cover_image_path = os.path.join(settings.MEDIA_ROOT, str(song.cover_image))
            private_mp3_file_path = os.path.join(private_playlist_dir, song.mp3_file.name.split('/')[-1])
            private_cover_image_path = os.path.join(private_playlist_dir, song.cover_image.name.split('/')[-1])
            
            
            shutil.move(mp3_file_path, private_mp3_file_path)
            shutil.move(cover_image_path, private_cover_image_path)

            return redirect('private_playlist')
    else:
        form = SongUploadForm()
    return render(request, 'private_song_upload.html', {'form': form})


@login_required
def download_song(request, song_id):
    song = get_object_or_404(Song, pk=song_id)
    song_path = os.path.join(settings.MEDIA_ROOT, str(song.mp3_file))
    response = redirect('home')
    response['Content-Disposition'] = f'attachment; filename="{os.path.basename(song_path)}"'
    response['X-Accel-Redirect'] = f'/protected/{str(song.mp3_file)}'
    return response

@login_required
def protected_song_upload(request):
    if request.method == 'POST':
        song_form = SongUploadForm(request.POST, request.FILES)
        protected_song_form = ProtectedSongForm(request.POST)
        
        if song_form.is_valid() and protected_song_form.is_valid():
            song = song_form.save(commit=False)
            song.uploaded_by = request.user
            song.save()
            
            protected_song = protected_song_form.save(commit=False)
            protected_song.song = song
            protected_song.save()
            
            
            protected_playlist_dir = os.path.join(settings.PROTECTED_PLAYLIST_ROOT, request.user.username)
            if not os.path.exists(protected_playlist_dir):
                os.makedirs(protected_playlist_dir)

            
            protected_mp3_file_path = os.path.join(protected_playlist_dir, str(song.mp3_file))
            protected_cover_image_path = os.path.join(protected_playlist_dir, str(song.cover_image))
            os.rename(song.mp3_file.path, protected_mp3_file_path)
            os.rename(song.cover_image.path, protected_cover_image_path)
            
            emails = protected_song.allowed_emails.split(',')
            valid_emails = []
            
            for email in emails:
                email = email.strip()
                if User.objects.filter(email=email).exists():
                    valid_emails.append(email)
            
            if valid_emails:
                send_mail(
                    'Protected Music File Shared with You',
                    f'You have been granted access to a protected music file. Log in to the Music Sharing Portal to access it.',
                    'from@example.com',
                    valid_emails,
                    fail_silently=True,
                )
                messages.success(request, 'Music file uploaded and shared successfully!')
            else:
                messages.warning(request, 'Music file uploaded successfully, but no valid email addresses found.')
            
            return redirect('protected_playlist')
    else:
        song_form = SongUploadForm()
        protected_song_form = ProtectedSongForm()
    
    return render(request, 'protected_song_upload.html', {'song_form': song_form, 'protected_song_form': protected_song_form})

@login_required
def protected_playlist(request):
    if request.method == 'POST':
        
        song = request.POST['song']
        playlist = ProtectedPlayList(user=request.user, song=song)
        playlist.save()
        return redirect('protected_playlist')

    
    playlist = ProtectedPlayList.objects.filter(user=request.user)
    return render(request, 'protected_playlist.html', {'playlist': playlist})

@login_required
def share_song(request, playlist_id):

    if request.method == 'POST':
        
        receiver_email = request.POST['receiver_email']
        song = Song.objects.filter(uploaded_by=request.user).first()
        receiver = User.objects.get(email=receiver_email)
        print('start')
        print(song)
        print(receiver)
        print(request.user)
        
        share_request = ShareRequest(sender=request.user, receiver=receiver, song=song)
        share_request.save()

        return redirect('private_playlist')

    
    return render(request, 'share_song.html',)
