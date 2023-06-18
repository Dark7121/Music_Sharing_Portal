from django.urls import path, include
from .views import home, signup, login_view, logout_view, song_upload, search, song_list, delete_song, private_playlist, private_song_upload, protected_playlist, protected_song_upload, share_song


urlpatterns = [
    path('', home, name='home'),
    path('signup/', signup, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('upload/', song_upload, name='upload'),
    path('search/', search, name='search'),
    path('songs/', song_list, name='song_list'),
    path('delete/<int:song_id>/', delete_song, name='delete_song'),
    path('private_playlist/', private_playlist, name='private_playlist'),
    path('private_playlist/upload/', private_song_upload, name='private_song_upload'),
    path('protected_playlist/', protected_playlist, name='protected_playlist'),
    path('protected_song_upload/', protected_song_upload, name='protected_song_upload'),
    path('share_song/<int:playlist_id>/', share_song, name='share_song'),
]
