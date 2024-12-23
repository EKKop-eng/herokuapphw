
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///items.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the database model
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

# Home route: List all items
@app.route('/')
def index():
    items = Item.query.all()  # Retrieve all items from the database
    return render_template('index.html', items=items)

# Add new item
@app.route('/add', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        name = request.form['name']
        new_item = Item(name=name)
        db.session.add(new_item)
        db.session.commit()
        return redirect(url_for('index'))  # Redirect to home after adding
    return render_template('add.html')

# Edit an existing item
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_item(id):
    item = Item.query.get_or_404(id)  # Retrieve the item by id
    if request.method == 'POST':
        item.name = request.form['name']
        db.session.commit()
        return redirect(url_for('index'))  # Redirect to home after editing
    return render_template('edit.html', item=item)

# Delete an item
@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete_item(id):
    item = Item.query.get_or_404(id)  # Retrieve the item by id
    if request.method == 'POST':
        db.session.delete(item)
        db.session.commit()
        return redirect(url_for('index'))  # Redirect to home after deleting
    return render_template('delete.html', item=item)

if __name__ == '__main__':
    # Create the database and tables if not already created
    with app.app_context():
        db.create_all()
    app.run(debug=True)
