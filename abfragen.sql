#Näherste / fernste Stationen

SELECT id,length,s.name,g.name FROM connections
LEFT JOIN stationen as s ON start=s.ref
LEFT JOIN stationen as g ON goal=g.ref
ORDER BY length ASC

# Suche nach Namen

SELECT *
FROM stationen WHERE name LIKE "%Spitt%";

#gpsprune

SELECT
  name,
  length,
  group_concat(id,".gpx" SEPARATOR " ")
FROM connections
  LEFT JOIN stationen ON (start = ref OR goal = ref)
WHERE ref = 906
ORDER BY length

#(vermutlich) abgelegenste Stationen

SELECT *
FROM (SELECT
        name,
        length,ref
      FROM connections
        LEFT JOIN stationen ON (start = ref OR goal = ref)
      ORDER BY length ASC ) as x
GROUP BY ref
ORDER BY length ASC