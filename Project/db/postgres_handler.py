import psycopg2

class PostgresHandler:
    def __init__(self, host, dbname, user, password):
        self.conn = psycopg2.connect(host=host, database=dbname, user=user, password=password)
        self._create_table()

    def _create_table(self):
        with self.conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS products (
                    id SERIAL PRIMARY KEY,
                    title TEXT,
                    final_price NUMERIC,
                    rating FLOAT,
                    rating_count INTEGER,
                    seller TEXT
                )
            """)
            self.conn.commit()

    def insert_products(self, products):
        with self.conn.cursor() as cur:
            for product in products:
                cur.execute("""
                    INSERT INTO products (title, final_price, rating, rating_count, seller)
                    VALUES (%s, %s, %s, %s, %s)
                """, (product['title'], product['final_price'], product['rating'], product['rating_count'], product['seller']))
            self.conn.commit()

    def get_product_count(self):
        with self.conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM products")
            return cur.fetchone()[0]

    def close(self):
        self.conn.close()
