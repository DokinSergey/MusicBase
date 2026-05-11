Select Artist, PERFORMER, count(*), sum(count(*))over (partition by PERFORMER) as cnt
from PlaylistUpdatable 
Where playlist_name = 'mp3' AND LOCALE = 'En'
group by PERFORMER,Artist
order by cnt desc
