# alembic/env.py
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from app.models import Users, Posts, Comments,followers  # Import your models
from app.database import Base  # Make sure to import Base from your database file

# Load the configuration file for logging
config = context.config
fileConfig(config.config_file_name)

# Set up target_metadata for 'autogenerate' support
target_metadata = Base.metadata

# This function will run migrations in 'offline' mode
def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()

# This function will run migrations in 'online' mode
def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
