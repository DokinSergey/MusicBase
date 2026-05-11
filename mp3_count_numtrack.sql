--2026-04-25
select tracknumber,count(tracknumber)
from Playlist 
where playlist_name = 'mp3'
group by tracknumber
order by count(tracknumber)