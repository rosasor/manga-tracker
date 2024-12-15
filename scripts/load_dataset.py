import pandas as pd

# Load the dataset
manga_data = pd.read_csv('../data/mangaMAL.csv')

# Drop any unnecessary columns (e.g., index columns or unnamed columns)
manga_data = manga_data.loc[:, ~manga_data.columns.str.contains('^Unnamed')]

# Drop specific columns by name
columns_to_remove = ['start_date', 'end_date', 'scored_by', 'members', 'approved', 'created_at_before'
                     , 'updated_at', 'real_start_date', 'real_end_date', 'authors', 'serializations'
                     , 'background', 'title_japanese', 'title_english', 'title_synonyms']
manga_data.drop(columns=columns_to_remove, inplace=True)

# Inspect the data
print(manga_data.head())

# Handle missing data
# For numerical columns, fill missing values with 0
numerical_columns = ['score', 'volumes', 'chapters', 'favorites', 'sfw']
for col in numerical_columns:
    manga_data[col] = manga_data[col].fillna(0)

# For categorical columns, fill missing values with an empty string
categorical_columns = ['title', 'type', 'status', 'genres', 'themes', 'demographics', 'synopsis', 'main_picture', 'url']
for col in categorical_columns:
    manga_data[col] = manga_data[col].fillna('')

# Check the cleaned data
print(manga_data.head())
