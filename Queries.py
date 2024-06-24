class Queries:
    @staticmethod
    def get_nodes(driver, limit=5):
        cypher = "MATCH (n) RETURN n LIMIT $limit"
        return driver.query(cypher, {"limit": limit})
