
SELECT MAX(Salary) AS SecondHighestSalary
FROM (
    SELECT Salary, DENSE_RANK() OVER (ORDER BY Salary DESC) AS rank
    FROM Employee
) ranked
WHERE rank = 2;
