from app import db


class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, index=True)
    content = db.Column(db.Text, nullable=True, index=True)
    is_complete = db.Column(db.Boolean)
    user_id = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Todo {}>'.format(self.user_id)

    def to_dict(self):
        todo_data = {}
        todo_data['id'] = self.id
        todo_data['name'] = self.name
        todo_data['content'] = self.content
        todo_data['is_complete'] = self.is_complete

        return todo_data
