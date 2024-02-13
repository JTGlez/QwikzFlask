from database.db import get_conn
from .entities.Student import Student

class StudentModel:

    @classmethod
    def register_student(self, student_uid: str):
        try:
            conn = get_conn()
            with conn.cursor() as cursor:
                cursor.execute("""INSERT INTO STUDENT (STUDENT_UID) 
                                VALUES (%s)""", (student_uid,))
            affected_rows = cursor.rowcount
            # Commit the changes to the database and close the connection
            conn.commit()
            conn.close()

            return affected_rows

        except Exception as e:
            raise Exception(e)
