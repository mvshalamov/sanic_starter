"""

"""

from yoyo import step

__depends__ = {'__init__'}

steps = [
    step(
        """
          CREATE TABLE test_table (
              id serial,
              name text NOT NULL
          );

        """,
        """
            DROP TABLE test_table;
        """
    )
]
