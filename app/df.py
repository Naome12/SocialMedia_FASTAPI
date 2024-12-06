import pandas as pd
import requests

try:
    # Fetch posts data
    posts_api = requests.get('http://127.0.0.1:8000/posts/')
    posts_api.raise_for_status()
    posts_api_data = posts_api.json()

    # Fetch users data
    users_api = requests.get('http://127.0.0.1:8000/users')
    users_api.raise_for_status()
    users_api_data = users_api.json()

    # Create DataFrames
    posts_df = pd.DataFrame(posts_api_data if isinstance(posts_api_data, list) else posts_api_data.get('posts', []))
    users_df = pd.DataFrame(users_api_data if isinstance(users_api_data, list) else users_api_data.get('users', []))

    # Inner Join (only matching rows from both DataFrames)
    inner_merged_df = pd.merge(posts_df, users_df, left_on='user_id', right_on='id', how='inner', suffixes=('_post', '_user'))
    # print("Inner Join Merged DataFrame:")
    # print(inner_merged_df)

    # Left Join (all rows from posts_df, matching rows from users_df)
    left_merged_df = pd.merge(posts_df, users_df, left_on='user_id', right_on='id', how='left', suffixes=('_post', '_user'))
    # print("\nLeft Join Merged DataFrame:")
    # print(left_merged_df)

    # Right Join (all rows from users_df, matching rows from posts_df)
    right_merged_df = pd.merge(posts_df, users_df, left_on='user_id', right_on='id', how='right', suffixes=('_post', '_user'))
    # print("\nRight Join Merged DataFrame:")
    # print(right_merged_df)

    # print(inner_merged_df.isnull().sum())
    # print(left_merged_df.dtypes)
    # inner_merged_df.ffill()
    # inner_merged_df['Dob'] = inner_merged_df['Dob'].astype(int)
    inner_merged_df['Dob'] = pd.to_numeric(inner_merged_df['Dob'],errors="coerce",downcast="integer")
    inner_merged_df['created_at_post'] = pd.to_numeric(inner_merged_df['created_at_post'],errors='coerce',downcast="integer")
    inner_merged_df['username'] = pd.to_numeric(inner_merged_df['username'],errors='coerce',downcast="integer")
    inner_merged_df['email'] = pd.to_numeric(inner_merged_df['email'],errors='coerce',downcast="integer")
    inner_merged_df['bio'] = pd.to_numeric(inner_merged_df['bio'],errors='coerce',downcast="integer")
    inner_merged_df['profile_picture'] = pd.to_numeric(inner_merged_df['profile_picture'],errors='coerce',downcast="integer")
    inner_merged_df['created_at_user'] = pd.to_numeric(inner_merged_df['created_at_user'],errors='coerce',downcast="integer")
    inner_merged_df['user'] = pd.to_numeric(inner_merged_df['user'],errors='coerce',downcast="integer")
    # print(inner_merged_df.dtypes)
    # print(inner_merged_df.isnull().sum())
    print(inner_merged_df.head())
    #backward fill and forward fill

except requests.exceptions.RequestException as e:
    print(f"Error fetching data from API: {e}")

except Exception as ex:
    print(f"An unexpected error occurred: {ex}")
