--Загрузка плейлиста 2025-08-08
Update PlaylistUpdatable 
Set tracknumber = 
(Select NewTrack From CurPlaylist Where PlaylistUpdatable.artist =  CurPlaylist.Artist and PlaylistUpdatable.title = CurPlaylist.Title )
Where (PlaylistUpdatable.playlist_name = 'Dokin');
