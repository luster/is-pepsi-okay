SELECT mid,title
FROM Movies
WHERE mid IN (
	SELECT DISTINCT(mid) 
	FROM Movies 
	WHERE mid IN (
		SELECT mid 
		FROM Is_Genre 
		WHERE gid IN (
			SELECT gid 
			FROM Likes_Genre 
			WHERE uid=%20
			ORDER BY urating DESC
		)
	)
	OR mid IN (
		SELECT mid
		FROM Involved_In
		WHERE pid IN (
			SELECT pid
			FROM Likes_Person
			WHERE uid=%20
			ORDER BY urating DESC
		)
	)
	OR mid IN (
		SELECT mid
		FROM Involved_In
		WHERE pid IN (
			SELECT pid
			FROM Involved_In
			JOIN Has_Watched
			ON Involved_In.mid=Has_Watched.mid
			WHERE uid=%20
			ORDER BY urating DESC
		)
	)		
)
AND mid NOT IN (
	SELECT mid
	FROM Has_Watched 
	WHERE uid=%20
);