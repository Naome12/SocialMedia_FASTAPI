from faker import Faker
import random
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.Posts import Post
from app.models.Users import User

fake = Faker()

def generate_unique_username(existing_usernames):
    """
    Generate a unique username not already in the provided set.

    :param existing_usernames: Set of usernames to ensure uniqueness
    :return: Unique username
    """
    while True:
        username = fake.user_name()
        if username not in existing_usernames:
            existing_usernames.add(username)
            return username

def generate_users_and_posts(
    db: Session, 
    num_users=495000, 
    num_posts=495000, 
    post_image_probability=0.8, 
    batch_size=1000,
    post_date_range=("-1y", "now")
):
    """
    Generate synthetic users and posts with validation and fallback values to prevent empty fields.

    :param db: Database session
    :param num_users: Number of users to generate
    :param num_posts: Number of posts to generate
    :param post_image_probability: Probability of a post having an image URL
    :param batch_size: Number of records to commit per batch
    :param post_date_range: Tuple specifying the date range for post creation
    """
    try:
        # Track existing usernames to ensure uniqueness
        existing_usernames = set()
        users = []

        # Generate users
        for _ in range(num_users):
            username = generate_unique_username(existing_usernames)
            email = fake.unique.email()
            bio = fake.text(max_nb_chars=100) if fake.text(max_nb_chars=100).strip() else "No bio provided"
            profile_picture = fake.image_url() or "https://example.com/default-profile-pic.jpg"
            Dob = fake.date_of_birth(minimum_age=18, maximum_age=80)

            user = User(
                username=username,
                email=email,
                bio=bio,
                profile_picture=profile_picture,
                Dob=Dob,
            )
            users.append(user)

            # Batch commit users
            if len(users) % batch_size == 0:
                try:
                    db.bulk_save_objects(users)
                    db.commit()
                    users.clear()
                except IntegrityError as e:
                    db.rollback()
                    print(f"IntegrityError during user insertion: {e}")
        
        # Save any remaining users
        if users:
            try:
                db.bulk_save_objects(users)
                db.commit()
            except IntegrityError as e:
                db.rollback()
                print(f"IntegrityError during final user insertion: {e}")
        print(f"{num_users} users generated!")

        # Fetch user IDs for post assignment
        user_ids = [user.id for user in db.query(User.id).all()]

        # Generate posts
        posts = []
        for _ in range(num_posts):
            user_id = random.choice(user_ids)
            content = fake.text(max_nb_chars=200) if fake.text(max_nb_chars=200).strip() else "Default post content"
            image_url = fake.image_url() if random.random() < post_image_probability else None
            created_at = fake.date_time_between(start_date=post_date_range[0], end_date=post_date_range[1])

            post = Post(
                user_id=user_id,
                content=content,
                image_url=image_url,
                created_at=created_at,
            )
            posts.append(post)

            # Batch commit posts
            if len(posts) % batch_size == 0:
                try:
                    db.bulk_save_objects(posts)
                    db.commit()
                    posts.clear()
                except IntegrityError as e:
                    db.rollback()
                    print(f"IntegrityError during post insertion: {e}")

        # Save any remaining posts
        if posts:
            try:
                db.bulk_save_objects(posts)
                db.commit()
            except IntegrityError as e:
                db.rollback()
                print(f"IntegrityError during final post insertion: {e}")
        print(f"{num_posts} posts generated!")

    except Exception as e:
        db.rollback()
        print(f"An unexpected error occurred: {e}")
