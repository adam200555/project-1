"""Project 1 - seeds a small school graph in Neo4j and queries it.
Run: python app.py
"""
from neo4j import GraphDatabase

URI = "bolt://localhost:7687"
AUTH = ("neo4j", "password123")

SEED = """
MERGE (adam:Student {name:'Adam'})
MERGE (sara:Student {name:'Sara'})
MERGE (omar:Student {name:'Omar'})
MERGE (java:Course {name:'Java'})
MERGE (nosql:Course {name:'NoSQL'})
MERGE (alami:Teacher {name:'Mr Alami'})
MERGE (adam)-[:FRIEND_OF]->(omar)
MERGE (adam)-[:ENROLLED_IN]->(java)
MERGE (adam)-[:ENROLLED_IN]->(nosql)
MERGE (sara)-[:ENROLLED_IN]->(nosql)
MERGE (omar)-[:ENROLLED_IN]->(java)
MERGE (alami)-[:TEACHES]->(nosql)
"""

QUERY = """
MATCH (s:Student)-[:ENROLLED_IN]->(c:Course)
RETURN s.name AS student, collect(c.name) AS courses
ORDER BY student
"""


def main():
    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        driver.verify_connectivity()
        driver.execute_query(SEED)  # MERGE = safe to run many times
        records, _, _ = driver.execute_query(QUERY)
        for r in records:
            print(f"{r['student']}: {', '.join(r['courses'])}")


if __name__ == "__main__":
    main()
