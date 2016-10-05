topSQL = {
    "shortestConnections": """
SELECT
  id,
  s.name,
  g.name,
  length

FROM connections
  LEFT JOIN stationen AS s ON start = s.ref
  LEFT JOIN stationen AS g ON goal = g.ref

WHERE start != goal
ORDER BY length ASC
LIMIT 10
""",
    "farAway": """
SELECT *
FROM (SELECT
        name,
        length,
        ref
      FROM connections
        LEFT JOIN stationen ON (start = ref OR goal = ref)
      WHERE start != goal
      ORDER BY length ASC) AS x
GROUP BY ref
ORDER BY length DESC"""
}


def helloworld(cursor, top):
    cursor.execute(topSQL[top])

    return cursor.fetchall()
