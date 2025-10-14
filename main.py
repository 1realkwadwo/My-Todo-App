from flask import Flask, render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy

# Create a Flask application instance
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(200), default='backlog')

    def __repr__(self):
        return f'<Task {self.content}>'
    
with app.app_context():
        db.create_all()  


# Define a route for the home page
@app.route('/home')
def index():
    backlog = Task.query.filter_by(status='backlog').all()
    in_progress = Task.query.filter_by(status='in_progress').all()
    done = Task.query.filter_by(status='done').all()
    return render_template('index.html', backlog=backlog, in_progress=in_progress, done=done)


@app.route('/add_task', methods = ['POST'])
def add():
    content = request.form['content']
    new_task = Task(content=content)
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for('index'))
 
    # tasks = Task.query.all()
    # return render_template('index.html',tasks=tasks)

@app.route('/delete/<int:task_id>', methods=['POST','GET'])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/update/<int:task_id>/<new_status>')
def update_status(task_id, new_status):
    task = Task.query.get_or_404(task_id)
    task.content = new_status
    db.session.commit()
    return redirect(url_for('index'))


# Run the application

if __name__ == '__main__':
    app.run(debug=True)
