import pandas as pd
from sqlalchemy.orm import Session
from app.models.Posts import Post
from app.models.Users import User
from sklearn.preprocessing import LabelEncoder, StandardScaler

def preprocess_posts(db: Session, limit=100000):
    """
    Fetch, preprocess, and engineer features for posts and user data.
    
    :param db: Database session
    :param limit: Number of posts to fetch
    :return: Preprocessed DataFrame
    """
    # Fetch posts and their associated users
    posts = db.query(Post).limit(limit).all()
    users = {user.id: user for user in db.query(User).all()}

    # Convert posts to a list of dictionaries
    data = [
        {
            "post_id": post.id,
            "user_id": post.user_id,
            "username": users[post.user_id].username if post.user_id in users else "Unknown",
            "content": post.content,
            "image_url": post.image_url,
            "created_at": post.created_at,
            "content_length": len(post.content) if post.content else 0,
            "has_image": 0 if not post.image_url else 1,
            # Add user-level feature - e.g., user's number of posts
            "user_post_count": sum(1 for p in posts if p.user_id == post.user_id)
        }
        for post in posts
    ]

    # Convert to Pandas DataFrame
    df = pd.DataFrame(data)

    # Handle missing values
    df['content'].fillna("No Content", inplace=True)
    df['image_url'].fillna("No Image", inplace=True)

    # Feature Engineering: Normalize content length (Min-Max scaling)
    df['content_length_normalized'] = (df['content_length'] - df['content_length'].min()) / (
        df['content_length'].max() - df['content_length'].min()
    )

    # Feature Engineering: Add day of the week (for created_at)
    df['day_of_week'] = pd.to_datetime(df['created_at']).dt.dayofweek

    # Encoding: User-level encoding using LabelEncoder for 'username' (if applicable)
    le = LabelEncoder()
    df['user_encoded'] = le.fit_transform(df['username'])

    # Optionally scale numerical features like content_length_normalized
    scaler = StandardScaler()
    df['scaled_content_length'] = scaler.fit_transform(df[['content_length_normalized']])

    return df
