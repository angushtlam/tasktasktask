from flask_socketio import emit

from app import db, socketio
from app.models import TaskList


@socketio.on("get_task_lists")
def get_task_lists():
    task_lists = TaskList.query.all()
    emit("get_task_lists",
         {"task_lists": [task_list.as_json for task_list in task_lists]})


@socketio.on("create_task_list")
def create_task_list(data):
    title = data.get("title")
    description = data.get("description", "")
    if title is None:
        emit("create_task_list", {"error": "Task lists must have a title."})
    else:
        task_list = TaskList(title, description)
        db.session.add(task_list)
        db.session.commit()
        emit("create_task_list", {"task_list": task_list.as_json}, broadcast=True)


@socketio.on("get_task_list")
def get_task_list(data):
    task_list = TaskList.query.filter_by(id=data.get("id")).first()
    if task_list is None:
        emit("get_task_list", {"error": "Task list not found."})
    else:
        emit("get_task_list", {"task_list": task_list.as_json})


@socketio.on("update_task_list")
def update_task_list(data):
    task_list = TaskList.query.filter_by(id=data.get("id")).first()
    if task_list is None:
        emit("update_task_list", {"error": "Task list not found."})
    else:
        task_list.title = data.get("title", task_list.title)
        task_list.description = data.get("description", task_list.description)
        db.session.commit()
        emit("update_task_list", {"task_list": task_list.as_json}, broadcast=True)


@socketio.on("delete_task_list")
def delete_task_list(data):
    task_list = TaskList.query.filter_by(id=data.get("id")).first()
    if task_list is None:
        emit("delete_task_list", {"error": "Task list not found."})
    else:
        db.session.delete(task_list)
        db.session.commit()
        emit("delete_task_list", {"task_list": {"id": data["id"]}}, broadcast=True)
