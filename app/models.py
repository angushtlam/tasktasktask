from app import db


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String, nullable=False)
    is_complete = db.Column(db.Boolean, default=False)
    list_id = db.Column(db.Integer, db.ForeignKey("task_list.id"), nullable=False)
    sublist_id = db.Column(db.Integer, db.ForeignKey("task_list.id"), unique=True)

    list = db.relationship("TaskList", backref=db.backref("tasks", lazy=False), foreign_keys=[list_id])
    sublist = db.relationship("TaskList", foreign_keys=[sublist_id])

    def as_json(self):
        return {
            "id": self.id,
            "description": self.description,
            "is_complete": self.is_complete,
            "list_id": self.list_id,
            "sublist_id": self.sublist_id,
        }


class TaskList(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    def as_json(self):
        return {"id": self.id}