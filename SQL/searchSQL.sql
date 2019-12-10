SELECT count(CAMIS)
From landmarks,restuarants
WHERE centerLogitude -restuarants.longitude <= 0.02 and centerLogitude -restuarants.longitude >= -0.02
and centerLatitude -restuarants.latitude <= 0.02 and centerLatitude -restuarants.latitude >= -0.02
and (landmarks.objectID = 1 or landmarkName ilike 'Decker Farmhouse')
and CAMIS not in (
Select CAMIS
From inspections
where extract(month from inspectiondate) =2019
  );

select distinct landmarkname, sum(ct)/count(restuarants.CAMIS), count(restuarants.CAMIS)
from landmarks,
restuarants,
(Select count(CAMIS) as ct, CAMIS
From inspections
Group By CAMIS) ctCAMIS
WHERE centerLogitude -restuarants.longitude <= 0.02 and centerLogitude -restuarants.longitude >= -0.02
and centerLatitude -restuarants.latitude <= 0.02 and centerLatitude -restuarants.latitude >= -0.02
and ctCAMIS.CAMIS = restuarants.CAMIS
and restuarants.CAMIS in (
SELECT CAMIS
FROM grades
WHERE grade ='A'
  )
Group by landmarkname
order by sum(ct)/count(restuarants.CAMIS), count(restuarants.CAMIS) DESC;
