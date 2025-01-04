SELECT title FROM movies
JOIN stars ON stars.movie_id = movies.id
JOIN people ON people.id = stars.person_id
WHERE people.name IN ('Bradley Cooper', 'Jennifer Lawrence')
GROUP BY (movies.title)
HAVING COUNT(DISTINCT people.name) = 2;
