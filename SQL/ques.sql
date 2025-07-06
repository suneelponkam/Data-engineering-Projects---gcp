1. How to retrieve the second-highest salary of an employee? 

SELECT MAX(salary)  
FROM employees  
WHERE salary < (SELECT MAX(salary) FROM employees); 

select distinct from employees
order by salary DESC
limit 1 offset 1;

select salary
from (
    select salary, dense_rank() over(order by salary) as ranked_salary
 from employees )
where ranked_salary = 2;

2. retrieves all employees whose salary is greater than the average salary in the employees table?

SELECT *  
FROM employees  
WHERE salary > (SELECT AVG(salary) FROM employees);

with CTE_Mode as (
    selct avg(salary) as avg_sal from employees
) 
select * 
from employees, CTE_Mode
where employees.salary > CTE_Mode.avg_sal;


3.. Write a query to display the current date and time in?

select current_timestamp();


4.How to find duplicate records in a table? 

select department,count(*)
FROM employees
GROUP BY department
HAVING count(*) > 1;

5.How can you delete duplicate rows in   ?

WITH CTE AS ( 
    SELECT column_name,  
           ROW_NUMBER() OVER (PARTITION BY column_name ORDER BY column_name) AS row_num 
    FROM table_name 
) 
DELETE FROM CTE WHERE row_num > 1;


6.How to get the common records from two tables? 

SELECT name from employees
intersect
select name from employees1;

select a.name
from employees a
inner JOIN
employees1 b
where a.name = b.name;


7.How to retrieve the last 10 records from a table?

select * from employees
order by employee_id DESC
limit 10;


8. TOP 5 highest salaries?

select * from employees
Order by salary DESC
limit 5;

9.How to calculate the total salary of all employees? 

selct sum(salary) as sum_salary
from employees;

10: How to write a query to find all employees who joined in the year 2020? 

select * from employees
where year(join_date) = 2020;

11.Write a query to find employees whose name starts with 'A'?

select * from employees
where name like 'A%';


12. How can you find the employees who do not have a manager? 

select * from employees
where maanager_id IS NULL;

13.How to find the department with the highest number of employees? 

select department_id, count(*)
from employees
group by department_id
order by count(*) DESC
limit 1;

14. How to get the count of employees in each department? 

select department,count(*) as emp_cnt
FROM employees
group by department;

15.Write a query to fetch employees having the highest salary in each 
department. 
SELECT department_id, employee_id, salary
FROM (
    SELECT *,
           RANK() OVER (PARTITION BY department_id ORDER BY salary DESC) AS rnk
    FROM employees
) ranked
WHERE rnk = 1;
