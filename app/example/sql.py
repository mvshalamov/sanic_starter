INSERT_SQL = """
    INSERT INTO test_table (name)
    VALUES ($1)
    RETURNING id;
"""

GET_SQL = """
    SELECT * FROM test_table;
"""
