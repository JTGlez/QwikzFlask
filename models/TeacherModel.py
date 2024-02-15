
from database.db import get_conn
from .entities.Teacher import Teacher


class TeacherModel:

    @classmethod
    def register_teacher(self, teacher_uid: str):
        try:
            conn = get_conn()
            with conn.cursor() as cursor:
                cursor.execute("""INSERT INTO TEACHER (TEACHER_UID) 
                                VALUES (%s)""", (teacher_uid,))
            affected_rows = cursor.rowcount
            # Commit the changes to the database and close the connection
            conn.commit()
            conn.close()

            return affected_rows

        except Exception as e:
            raise Exception(e)
