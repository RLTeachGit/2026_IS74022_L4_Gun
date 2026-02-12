with results as (
select
ANY_VALUE(user_id) as user_id,
session_id,
countif(lower(event_type)=lower("pickup")) as pickups,
countif(lower(event_type)='enter' and contains_substr(lower(event_data),lower('BehindBlock.Box"'))) as Secrets,
countif(lower(event_type)='fire' and contains_substr(lower(event_data),lower('Out of ammo'))) as NoAmmo,
TIMESTAMP_DIFF(max(created_at),min(created_at), SECOND) as playtime_seconds,
min(created_at) as created_at
from `ue5test-486811.UE5Analytics.Event_log`
group by session_id)
select
* from results
order by results.created_at

