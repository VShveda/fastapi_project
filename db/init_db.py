from db.database import Base, engine
from posts.models import Post
from user.models import User


print("Creating database tables...")
Base.metadata.create_all(bind=engine)
print("Database tables created successfully!")
