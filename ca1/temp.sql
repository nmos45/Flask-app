SELECT *
FROM Netflix


SELECT *
FROM Amazon

select * from Disney


    SELECT title FROM Netflix
    UNION
    SELECT title FROM Amazon
    UNION
    SELECT title FROM Disney

SELECT *
from reviews

select *
FROM users

select *
FROM admin

INSERT INTO admin(admin_id,password)
VALUES('CertifiedMovieReviewer','ILOvemovies123')

SELECT password FROM Admin

SELECT * FROM Netflix UNION SELECT * FROM Amazon UNION SELECT * FROM Disney
ORDER BY score DESC

SELECT * FROM DisneyCast

SELECT * FROM Amazon JOIN AmazonCast JOIN reviews
ON Amazon.title = AmazonCast.title AND AmazonCast.title = reviews.film

SELECT * FROM Disney JOIN DisneyCast JOIN reviews
ON Disney.title = DisneyCast.title AND DisneyCast.title= reviews.film

UPDATE Score
SET score = 


SELECT *
FROM Score

Select * from Netflix

SELECT DISTINCT(film) From reviews;

SELECT * 
FROM NET





ALL,South Africa,Canada,Mexico,India,France,Japan,Italy,Romania,Australia,United Kingdom,United States

SELECT * FROM Netflix
WHERE title = "Chappie" and country like "%South Africa%"