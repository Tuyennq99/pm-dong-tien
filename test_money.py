import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.db import connection

with connection.cursor() as c:
    c.execute("DROP TABLE IF EXISTS test_money")

    c.execute("""
        CREATE TABLE test_money (
            id INT AUTO_INCREMENT PRIMARY KEY,
            amount DECIMAL(20,2)
        )
    """)

    c.execute("""
        INSERT INTO test_money (amount)
        VALUES
        (1000.00),
        (1000000.00),
        (10000000000.25),
        (999999999999999999.99)
    """)

    c.execute("SELECT amount FROM test_money ORDER BY id")
    print(c.fetchall())

    c.execute("SELECT SUM(amount) FROM test_money")
    print("SUM =", c.fetchone()[0])