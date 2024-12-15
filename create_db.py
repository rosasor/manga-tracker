from app import create_app, db

# Create the app instance
app = create_app()

# Create all tables in the database
with app.app_context():
    db.create_all()

print("Database tables created!")
