-- Дата загрузки трека 2025-08-08
Update PlaylistUpdatable Set comment = substr(file_created,0,11)
--select substr(file_created,0,11) as dateins ,comment,length(comment) from PlaylistUpdatable 
Where playlist_name = 'Dokin' and comment ISNULL
--length(comment) != 10