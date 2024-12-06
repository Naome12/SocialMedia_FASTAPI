import pandas as pd
import requests
from sklearn.preprocessing import LabelEncoder
from datetime import datetime

# Define API URLs
POSTS_URL = "http://127.0.0.1:8000/posts/"
USERS_URL = "http://127.0.0.1:8000/users"

try:
    # Fetch posts data
    posts_response = requests.get(POSTS_URL)
    posts_response.raise_for_status()
    posts_data = posts_response.json()

    # Fetch users data
    users_response = requests.get(USERS_URL)
    users_response.raise_for_status()
    users_data = users_response.json()

    # Create DataFrames
    posts_df = pd.DataFrame(posts_data if isinstance(posts_data, list) else posts_data.get("posts", []))
    users_df = pd.DataFrame(users_data if isinstance(users_data, list) else users_data.get("users", []))

    # Inner Join (only matching rows from both DataFrames)
    inner_merged_df = pd.merge(
        posts_df,
        users_df,
        left_on="user_id",
        right_on="id",
        how="inner",
        suffixes=("_post", "_user")
    )

    # Task 1: Return 500,000 rows in your dataset
    # Expand dataset by duplicating rows until it has 500,000 rows
    while len(inner_merged_df) < 500000:
        inner_merged_df = pd.concat([inner_merged_df, inner_merged_df.sample(len(inner_merged_df))], ignore_index=True)
    inner_merged_df = inner_merged_df[:500000]

    # Task 2: Describe your dataset
    # Display dataset information and summary
    print("Dataset Information:")
    print(inner_merged_df.info())
    print("\nDataset Description:")
    print(inner_merged_df.describe(include='all'))

    # Task 3: Find and replace null values
    # Replace null values with 'Unknown'
    inner_merged_df.fillna("Unknown", inplace=True)

    # Task 4: Perform basic data preprocessing
    # Ensure usernames and other text columns are not encoded
    for col in ['username', 'email', 'content', 'bio']:
        if col in inner_merged_df.columns:
            inner_merged_df[col] = inner_merged_df[col].astype(str)

    # Replace newlines in text columns to ensure each row is on one line
    for col in ['content', 'bio']:
        if col in inner_merged_df.columns:
            inner_merged_df[col] = inner_merged_df[col].str.replace('\n', ' ', regex=True)

    # Reorder columns for consistency
    cols = ['id_post', 'user_id'] + [col for col in inner_merged_df.columns if col not in ['id_post', 'user_id']]
    inner_merged_df = inner_merged_df[cols]

    # Task 5: Create new features
    # Creating features such as 'Age', 'Age Group', 'Month of Birth', and 'Day of Week'
    if "Dob" in inner_merged_df.columns:
        inner_merged_df["Dob"] = pd.to_datetime(inner_merged_df["Dob"], errors='coerce')
        current_date = datetime.now()
        inner_merged_df["Age"] = (current_date - inner_merged_df["Dob"]).dt.days // 365

        # Create Age Group bins
        bins = [0, 18, 25, 35, 45, 55, 65, 100]
        labels = ["0-17", "18-25", "26-35", "36-45", "46-55", "56-65", "65+"]
        inner_merged_df["Age Group"] = pd.cut(inner_merged_df["Age"], bins=bins, labels=labels, right=False)

        # Extract Month of Birth and Day of Week
        inner_merged_df["Month of Birth"] = inner_merged_df["Dob"].dt.month
        inner_merged_df["Day of Week"] = inner_merged_df["Dob"].dt.dayofweek

    # Save final dataset to CSV (avoid multiline rows)
    inner_merged_df.to_csv("merged_dataset_cleaned.csv", index=False, quoting=1)  # quoting=1 ensures quotes around text fields
    print("\nMerged dataset saved as 'merged_dataset_cleaned.csv'.")

except requests.exceptions.RequestException as e:
    print(f"Error fetching data from API: {e}")
except Exception as ex:
    print(f"An unexpected error occurred: {ex}")
