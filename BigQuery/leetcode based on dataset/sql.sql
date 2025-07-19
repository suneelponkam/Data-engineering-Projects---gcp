 
 -- the 2nd driver id: similar to 2nd highest salary 
 
 select distinct driverid,concat(forename,' ',surname) as driver_name from cap_dataset.drivers_backup
 order by driverid asc
 limit 1 offset 1;


 -- the nth driver id: similar to nth highest salary

 SELECT driverid, concat(forename,' ',surname) as driver_name
FROM (
  SELECT driverid,forename,surname, DENSE_RANK() OVER (ORDER BY driverid ASC) AS rnk
  FROM `neural-service-464913-n3.cap_dataset.drivers_backup`
) ranked_data
WHERE rnk = 2;

-- youngest driver

select fullname,dob
from cap_dataset.drivers
order by dob desc
limit 1;

-- count national wise

SELECT nationality, COUNT(*) AS num_drivers
FROM cap_dataset.drivers
group by nationality
order by num_drivers desc;


--- name starts with N and nationality is German

SELECT forename, surname
FROM drivers
WHERE nationality = 'German' AND forename LIKE 'N%';


