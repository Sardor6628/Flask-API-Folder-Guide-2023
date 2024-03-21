from flask import request, Response, json, Blueprint
from src.models.task_model import Task
from src.models.user_model import User
from src import bcrypt, db
from datetime import datetime

tasks = Blueprint("tasks", __name__)


@tasks.route('/getAll', methods=["GET"])
def get_users():
    try:
        list_of_tasks = []
        query_of_tasks = Task.query.all()
        for _task in query_of_tasks:
            list_of_tasks.append(_task.to_json())
        return Response(
            response=json.dumps(
                {'status': "success", "tasks": list_of_tasks}),
            status=200,
            mimetype='application/json')
    except Exception as e:
        return Response(
            response=json.dumps({'status': "failed", "message": "Error Occurred", "error": str(e)}),
            status=500,
            mimetype='application/json'
        )


@tasks.route('/create', methods=["POST"])
def create():
    try:
        data = request.json
        is_right_credentials = "title" in data and "body" in data and "user_id" in data
        if not is_right_credentials:
            raise ValueError("Required parameters are missing")
        is_body_or_title_empty = len(data['body']) == 0 or len(data['title']) == 0
        if is_body_or_title_empty:
            raise ValueError("Some parameters are empty")
        get_user = User.query.filter_by(id=data['user_id']).first()
        if not get_user:
            raise ValueError("There is no such user")
        task_obj = Task(
            user_id=data["user_id"],
            title=data["title"],
            body=data['body'],
            created_at=datetime.now(),
            is_modified=False
        )
        db.session.add(task_obj)
        db.session.commit()
        return Response(
            status=200,
            response=json.dumps({"status": "success", "message": "Task created successfully"})
        )
    except Exception as e:
        return Response(
            response=json.dumps({'status': "failed", "message": "Error Occurred", "error": str(e)}),
            status=500,
            mimetype='application/json'
        )


@tasks.route('/update', methods=["POST"])
def update():
    try:
        data = request.json
        is_right_credentials = "title" in data and "body" in data and "user_id" in data and "id" in data
        if not is_right_credentials:
            raise ValueError("Some required parameters are missing")
        task = Task.query.filter_by(id=data['id']).first()
        if not task:
            raise ValueError("There is no task with such id")
        is_the_same_owner = task.user_id == data['user_id']
        if not is_the_same_owner:
            raise ValueError("This task doesn't belong to you")
        task.body = data['body']
        task.title = data['title']
        task.is_modified = True
        db.session.commit()
        return Response(
            response=json.dumps({'status': "success", "message": "Task has been updated!"}),
            status=200,
            mimetype='application/json'
        )
    except Exception as e:
        return Response(
            response=json.dumps({'status': "failed", "message": "Error Occurred", "error": str(e)}),
            status=500,
            mimetype='application/json'
        )


@tasks.route("/get-user-tasks", methods=["POST"])
def get_user_tasks():
    try:
        data = request.json
        is_right_credentials = "user_id" in data
        if not is_right_credentials:
            raise ValueError("Wrong credentials")
        _user = User.query.filter_by(id=data['user_id']).first()
        if not _user:
            raise ValueError("There is no such user")
        list_of_tasks = Task.query.filter_by(user_id=data['user_id'])
        payload = []
        for _task in list_of_tasks:
            payload.append(_task.to_json())
        return Response(
            status=200,
            mimetype='application/json',
            response=json.dumps({"status": "success", "message": "returned successfully", "result": payload})
        )
    except Exception as e:
        return Response(
            response=json.dumps({'status': "failed", "message": "Error Occurred", "error": str(e)}),
            status=500,
            mimetype='application/json')
