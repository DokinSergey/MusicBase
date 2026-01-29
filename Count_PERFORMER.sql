Select Artist, PERFORMER, count(*), sum(count(*))over (partition by PERFORMER) as cnt
from PlaylistUpdatable 
Where playlist_name = 'Dokin'
group by PERFORMER,Artist
order by cnt desc
