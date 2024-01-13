import sqlite3


class Database:
    def __init__(self, db_name: str):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.c = self.conn.cursor()
        self.setup()

    def setup(self):
        """Set up the database."""
        self.create_table("system_users", ["username TEXT", "password TEXT", "token TEXT"])

    def create_table(self, table_name: str, columns: list) -> None:
        """Create a table in the database.

        Args:
            table_name (str): Name of the table
            columns (list): List of columns
        """
        self.c.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(columns)})")
        self.conn.commit()

    def validate_token(self, token: str) -> bool:
        """Validate a token.

        Args:
            token (str): Token to validate

        Returns:
            bool: True if token is valid, False otherwise
        """
        token = token.replace('-', '')
        self.c.execute(f"SELECT * FROM `system_users` WHERE `token`='{token}'")
        return self.c.fetchone() is not None
