--2025-07-31
Select Artist, PERFORMER, count(*), sum(count(*))over (partition by PERFORMER) as cnt,sum(count(*))over (partition by locale) as lk, sum(count(*))over () as ali
from PlaylistUpdatable 
Where playlist_name = 'Dokin'
group by PERFORMER,Artist
order by cnt desc
