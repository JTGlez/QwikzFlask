import random
import string
from database.db import get_conn
from .entities.Group import Group


class GroupModel:

    # Allows the get_groups method to be called without creating an instance of the GroupModel class
    @classmethod
    def get_groups(self, teacher_uid: str):

        try:
            conn = get_conn()
            groups = []

            with conn.cursor() as cursor:

                cursor.execute("""
                    SELECT TEACHER_ID FROM TEACHER WHERE TEACHER_UID = %s""", (teacher_uid,))
                teacher_id = cursor.fetchone()[0]

                cursor.execute("""
                    SELECT * FROM QWIKZGROUP WHERE TEACHER_ID = %s""", (teacher_id,))
                rows = cursor.fetchall()

                for row in rows:
                    group = Group(row[0], row[1], row[2], row[3], row[4])
                    groups.append(group.to_JSON())

            conn.close()
            return groups

        except Exception as e:
            raise Exception(e)

    @classmethod
    def get_student_groups(self, student_uid: str):
        try:
            conn = get_conn()
            groups = []

            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT STUDENT_ID FROM STUDENT WHERE STUDENT_UID = %s""", (student_uid,))
                student_id = cursor.fetchone()[0]

                cursor.execute("""
                    SELECT QWIKZGROUP_ID FROM GROUP_STUDENT WHERE STUDENT_ID = %s""", (student_id,))
                group_ids = cursor.fetchall()

                for group_id in group_ids:
                    cursor.execute("""
                        SELECT GROUP_NAME, GROUP_CODE FROM QWIKZGROUP WHERE QWIKZGROUP_ID = %s""", (group_id[0],))
                    group = cursor.fetchone()
                    groups.append({
                        "group_name": group[0],
                        "group_code": group[1],
                    })

            conn.close()
            return groups

        except Exception as e:
            raise Exception(e)

    @classmethod
    def create_group(self, teacher_uid: str, group_name: str, group_code: str):
        try:
            conn = get_conn()

            # Create a random access token of length 12 with format "XXXX-XXXX-XXXX"
            access_token = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(4)) + '-' + ''.join(random.choice(
                string.ascii_uppercase + string.digits) for _ in range(4)) + '-' + ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(4))
            print(access_token)

            # Get the teacher's id by the uid
            with conn.cursor() as cursor:
                cursor.execute(
                    """SELECT TEACHER_ID FROM TEACHER WHERE TEACHER_UID = %s""", (teacher_uid,))
                teacher_id = cursor.fetchone()[0]

                # Create a group using the teacher's id
                cursor.execute("""INSERT INTO QWIKZGROUP (TEACHER_ID, GROUP_NAME, GROUP_CODE, ACCESS_TOKEN) 
                                VALUES (%s, %s, %s, %s)""", (teacher_id, group_name, group_code, access_token))

                affected_rows = cursor.rowcount

            # Commit the changes to the database and close the connection
            conn.commit()
            conn.close()

            return {
                "affected_rows": affected_rows,
                "group": {
                    "teacher_id": teacher_id,
                    "groupName": group_name,
                    "groupCode": group_code,
                    "accessToken": access_token
                }
            }

        except Exception as e:
            raise Exception(e)

    @classmethod
    def join_group(self, access_token: str, student_uid: str):

        try:
            conn = get_conn()

            with conn.cursor() as cursor:
                cursor.execute(
                    """SELECT STUDENT_ID FROM STUDENT WHERE STUDENT_UID = %s""", (student_uid,))
                student_id = cursor.fetchone()[0]

                cursor.execute(
                    """SELECT QWIKZGROUP_ID FROM QWIKZGROUP WHERE ACCESS_TOKEN = %s""", (access_token,))
                group_id = cursor.fetchone()[0]

                cursor.execute(
                    """INSERT INTO GROUP_STUDENT (STUDENT_ID, QWIKZGROUP_ID) VALUES (%s, %s)""", (student_id, group_id))

                cursor.execute(
                    """SELECT GROUP_NAME, GROUP_CODE, ACCESS_TOKEN FROM QWIKZGROUP WHERE QWIKZGROUP_ID = %s""", (group_id,))
                group = cursor.fetchone()

            conn.commit()
            conn.close()

            return {
                "ok": True,
                "group": {
                    "groupName": group[0],
                    "groupCode": group[1],
                    "accessToken": group[2]
                }
            }

        except Exception as e:
            raise Exception(e)
