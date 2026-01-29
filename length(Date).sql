-- Дата загрузки трека 2025-07-23
Update PlaylistUpdatable Set Date = substr(Date,0,5)
--select Date ,substr(Date,0,5) from PlaylistUpdatable 
Where playlist_name = 'Dokin' and length(Date) = 10