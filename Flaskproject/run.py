from flaskblog import app, init_db



if __name__ == '__main__':
    init_db()  # Initialize the database
    app.run(debug=True)
