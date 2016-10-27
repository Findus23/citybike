cache = {}

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
LIMIT %s OFFSET %s
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
ORDER BY length DESC
LIMIT %s OFFSET %s
"""
}


def helloworld(cursor, args):

    sql = topSQL[args["type"]]
    limit = int(args["pageSize"])
    offset = (int(args["pageNumber"]) - 1) * limit
    cursor.execute(sql, (limit, offset))
    return cursor.fetchall()
