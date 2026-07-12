-- Дата загрузки трека 2026-06-07
-- Update PlaylistUpdatable Set comment = substr(file_created,0,11)
select substr(file_created,0,11),comment,* from PlaylistUpdatable 
Where playlist_name = 'Dokin' and comment is null
-- Where playlist_name = 'Dokin' and trim(comment) != substr(file_created,0,11) 