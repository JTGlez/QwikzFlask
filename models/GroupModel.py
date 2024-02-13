from database.db import get_conn
from .entities.Group import Group


class GroupModel:

    # Allows the get_groups method to be called without creating an instance of the GroupModel class
    @classmethod
    def get_groups(self):

        try:
            conn = get_conn()
            groups = []

            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM groups LIMIT 10")
                rows = cursor.fetchall()

                for row in rows:
                    group = Group(row[0], row[1], row[2], row[3], row[4])
                    groups.append(group.to_JSON())

            conn.close()
            return groups

        except Exception as e:
            raise Exception(e)
