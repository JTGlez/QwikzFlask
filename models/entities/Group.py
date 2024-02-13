class Group():

    def __init__(self, group_id, teacher_id, group_name, group_code, access_token) -> None:
        self.group_id = group_id
        self.teacher_id = teacher_id
        self.group_name = group_name
        self.group_code = group_code
        self.access_token = access_token

    def to_JSON(self):
        """Serialize the Group object to JSON

        Returns:
            JSON: JSON representation of the Group object
        """
        return {
            "group_id": self.group_id,
            "teacher_id": self.teacher_id,
            "group_name": self.group_name,
            "group_code": self.group_code,
            "access_token": self.access_token
        }
