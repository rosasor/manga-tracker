import sys
import os

# Add the root project directory to the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd
from app import db  # Importing only db here
from models.manga import Manga
from app import create_app  # Import create_app to initialize the app

def import_csv_to_db():
    # Load the CSV data into a pandas DataFrame
    df = pd.read_csv(os.path.join(os.path.dirname(__file__), '..', 'data', 'mangaMAL.csv'))

    # Clean up the dataframe by dropping any unnecessary columns
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]  # Remove unnamed columns

    # Initialize the app and wrap the database interaction in the application context
    app = create_app()  # Initialize the Flask app
    with app.app_context():
        # Iterate over each row in the DataFrame and add it to the database
        for _, row in df.iterrows():
            manga = Manga(
                manga_id=row['manga_id'],
                name=row['title'],  # 'Name' column for the manga title
                type=row['type'],
                score=row['score'],
                status=row['status'],
                volumes=row['volumes'],
                chapters=row['chapters'],
                favorites=row['favorites'],
                sfw=row['sfw'],
                genre=row['genres'],
                theme=row['themes'],
                demographic=row['demographics'],
                synopsis=row['synopsis'],
                image=row['main_picture'],
                url=row['url'],
            )
            db.session.add(manga)

        # Commit the changes to the database
        db.session.commit()
        print("Data imported successfully.")

if __name__ == '__main__':
    import_csv_to_db()
