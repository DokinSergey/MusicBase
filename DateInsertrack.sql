-- Дата загрузки трека 2025-07-23
Update PlaylistUpdatable Set comment = substr(file_created,0,11)
-- select substr(file_created,0,11),* from PlaylistUpdatable 
Where playlist_name = 'Dokin' and trim(comment) != substr(file_created,0,11)