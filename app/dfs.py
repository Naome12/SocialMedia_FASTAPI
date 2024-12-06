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
    # print(posts_df)
    # print(users_df)

    # # Inner Join (only matching rows from both DataFrames)
    inner_merged_df = pd.merge(posts_df, users_df, left_on='user_id', right_on='id', how='inner', suffixes=('_post', '_user'))
    print(inner_merged_df)

    # # Feature Engineering
    # # 1. Email Length: Create a feature for the length of the user's email
    # inner_merged_df['email_length'] = inner_merged_df['email'].apply(len)

    # # 2. User-Post Time Difference: Assuming 'created_at_user' and 'created_at_post' are timestamps
    # inner_merged_df['user_post_difference'] = pd.to_datetime(inner_merged_df['created_at_post']) - pd.to_datetime(inner_merged_df['created_at_user'])
    # inner_merged_df['user_post_difference'] = inner_merged_df['user_post_difference'].dt.days  # Convert to days

    # # 3. Is Active: Assuming users with posts are active, mark users with at least one post as active
    # inner_merged_df['is_active'] = inner_merged_df['id_post'].apply(lambda x: 1 if pd.notnull(x) else 0)

    # # Handle missing values using ffill and bfill
    # inner_merged_df.ffill(inplace=True)  # Forward fill
    # inner_merged_df.bfill(inplace=True)  # Backward fill

    # # Print the final DataFrame
    # print(inner_merged_df.head())

except requests.exceptions.RequestException as e:
    print(f"Error fetching data from API: {e}")

except Exception as ex:
    print(f"An unexpected error occurred: {ex}")
