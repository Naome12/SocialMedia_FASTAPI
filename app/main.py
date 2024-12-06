from fastapi import FastAPI
from sqlalchemy.orm import Session
from app.database import init_db, SessionLocal
from .routes import user_routes, posts_routes, auth_routes, comments_routes
from app.utils.data_generator import generate_users_and_posts

app = FastAPI()

# Include API routes
app.include_router(user_routes.router)
app.include_router(posts_routes.router)
app.include_router(auth_routes.router)
app.include_router(comments_routes.router)

# Initialize database on startup
@app.on_event("startup")
def on_startup():
    init_db()  # Initialize database schema
    # db: Session = SessionLocal()
    # try:
    #     generate_users_and_posts(db, num_users=495000, num_posts=495000)  # Reduced data generation for startup
    # finally:
    #     db.close()



# import asyncio
# import aiohttp
# from faker import Faker
# import pandas as pd

# # URLs for creating users and posts
# users_url = "http://127.0.0.1:8000/users/createuser"
# posts_url = "http://127.0.0.1:8000/posts/createpost"
# login_url = "http://127.0.0.1:8000/auth/login"  # Assuming you have a login endpoint

# fake = Faker()

# # Generate a fake user
# def create_fake_user():
#     return {
#         "username": fake.user_name(),
#         "email": fake.email(),
#         "Dob": str(fake.date_of_birth(minimum_age=18, maximum_age=70)),
#         "password": fake.password(),
#         "bio": fake.text(max_nb_chars=100),
#         "profile_picture": fake.image_url(),
#     }

# # Generate a fake post for a user
# def create_fake_post(user_id):
#     return {
#         "content": fake.text(max_nb_chars=300),
#         "image_url": fake.image_url(),
#         "user_id": user_id
#     }

# # Login to get a JWT token
# async def login_user(session, user_data):
#     async with session.post(login_url, json={"username": user_data["username"], "password": user_data["password"]}) as response:
#         if response.status == 200:
#             login_response = await response.json()
#             token = login_response.get("access_token")
#             if token:
#                 return token
#             else:
#                 print("Failed to retrieve token")
#                 return None
#         else:
#             print(f"Login failed: {response.status}")
#             return None

# # Function to create a user
# async def create_user(session):
#     user_data = create_fake_user()  # Create fake user data
#     async with session.post(users_url, json=user_data) as response:
#         if response.status == 200:
#             user = await response.json()
#             print(f"User created: {user['id']}")
#             return user['id'], user_data
#         else:
#             error_message = await response.text()
#             print(f"Failed to create user: {response.status}, Error: {error_message}")
#             return None, None

# # Function to create a post
# async def create_post(session, user_id, token):
#     post_data = create_fake_post(user_id)  # Create fake post data
#     headers = {"Authorization": f"Bearer {token}"}  # Add token to headers
#     async with session.post(posts_url, json=post_data, headers=headers) as response:
#         if response.status == 201:
#             post = await response.json()
#             print(f"Post created for user {user_id}: {post['id']}")
#             return post['id'], post_data
#         else:
#             error_message = await response.text()
#             print(f"Failed to create post: {response.status}, Error: {error_message}")
#             return None, None

# # Main function to create users, login, and create posts
# async def main():
#     async with aiohttp.ClientSession() as session:
#         user_data_list = []
#         post_data_list = []

#         for i in range(500000):  # Loop for 500,000 users
#             print(f"Creating user and post {i+1}...")
#             user_id, user_data = await create_user(session)
#             if user_id:
#                 token = await login_user(session, user_data)  # Log in to get token
#                 if token:
#                     post_id, post_data = await create_post(session, user_id, token)  # Create post using token
#                     if post_id:
#                         # Merge user data and post data
#                         merged_data = {**user_data, **post_data}
#                         user_data_list.append(merged_data)  # Add merged data to list

#             if i % 100 == 0:  # Save progress every 100 users (you can adjust the number)
#                 print(f"Saving progress after {i+1} users.")
#                 # Save user_data_list and post_data_list to CSV (or database) here
#                 save_to_csv(user_data_list, i)

#         # Save to CSV after all users and posts are created
#         save_to_csv(user_data_list, "final")

#         print("User and post creation process completed.")

# # Function to save merged user and post data to CSV
# def save_to_csv(user_data_list, batch_number):
#     # Save merged data to CSV
#     df = pd.DataFrame(user_data_list)
#     df.to_csv(f'users_and_posts_batch_{batch_number}.csv', index=False)

# # Run the main function
# if __name__ == "__main__":
#     asyncio.run(main())
