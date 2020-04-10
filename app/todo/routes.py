from app import db
from flask import request, jsonify
from app.todo import todo as blueprint
from flask.views import MethodView
from app.todo.models import Todo
from app.auth.routes import login_required


def create_todo(user_id, name, content):
    try:
        new_todo = Todo()
        new_todo.user_id = user_id
        new_todo.name = name
        new_todo.content = content
        new_todo.is_complete = False

        db.session.add(new_todo)
        db.session.commit()

        return new_todo
    except:
        return False


class TodoAPI(MethodView):

    @login_required
    def get(self, current_user):
        todos = Todo.query.filter_by(user_id=current_user.id).all()
        result = []
        for todo in todos:
            result.append(todo.to_dict())

        return jsonify({'todos': result})

    @login_required
    def post(self, current_user):
        data = request.get_json()
        name = data.get('name', None)
        content = data.get('content', None)
        if name:
            new_todo = create_todo(current_user.id, name, content)
            if new_todo:
                return jsonify({'message': 'Successful', 'todo': new_todo.to_dict()})
            else:
                return jsonify({'error': 'Something wrong'}), 404
        else:
            return jsonify({'error': 'Name must be not none'}), 404


blueprint.add_url_rule(rule='/',
    view_func=TodoAPI.as_view('todo_api'))


class TodoDetailAPI(MethodView):

    @login_required
    def get(self, current_user, todo_id):
        '''Get detail todo with todo id'''
        todo = Todo.query.filter_by(user_id=current_user.id, id=todo_id).first()
        if todo:
            return jsonify({'message': 'Successful!', 'todo': todo.to_dict()})
        else:
            return jsonify({'error': 'Todo not found'}), 404

    @login_required
    def post(self, current_user, todo_id):
        '''Change detail todo with todo id'''
        data = request.get_json()
        name = data.get('name', None)
        content = data.get('content', None)
        if name:
            todo = Todo.query.filter_by(user_id=current_user.id, id=todo_id).first()
            if todo:
                todo.name = name
                todo.content = content
                db.session.commit()
                return jsonify({'message': 'Successful!', 'todo': todo.to_dict()})
            else:
                return jsonify({'error': 'Todo not found'}), 404
        else:
            return jsonify({'error': 'Name must be not none'}), 404

    @login_required
    def put(self, current_user, todo_id):
        '''Toggle todo'''
        todo = Todo.query.filter_by(user_id=current_user.id, id=todo_id).first()
        if todo:
            todo.is_complete = not todo.is_complete
            db.session.commit()
            return jsonify({'message': 'Successful'})
        else:
            return jsonify({'error': 'Todo not found'}), 404

    @login_required
    def delete(self, current_user, todo_id):
        todo = Todo.query.filter_by(user_id=current_user.id, id=todo_id).first()
        if todo:
            db.session.delete(todo)
            db.session.commit()
            return jsonify({'message': 'Successful'})
        else:
            return jsonify({'error': 'Todo not found'}), 404


blueprint.add_url_rule(rule='/<int:todo_id>',
    view_func=TodoDetailAPI.as_view('todo_detail_api'))
