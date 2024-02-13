class Student():

    def __init__(self, student_id, uid, profile_pic=None) -> None:
        self.student_id = student_id
        self.uid = uid
        self.profile_pic = profile_pic

    def to_JSON(self):
        """Serialize the Group object to JSON

        Returns:
            JSON: JSON representation of the Group object
        """
        return {
            "student_id": self.student_id,
            "uid": self.uid,
            "profile_pic": self.profile_pic
        }