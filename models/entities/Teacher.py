class Teacher():

    def __init__(self, teacher_id, uid, profile_pic=None ) -> None:
        self.teacher_id = teacher_id
        self.uid = uid
        self.profile_pic = profile_pic

    def to_JSON(self):
        """Serialize the Group object to JSON

        Returns:
            JSON: JSON representation of the Group object
        """
        return {
            "teacher_id": self.teacher_id,
            "uid": self.uid,
            "profile_pic": self.profile_pic
        }
