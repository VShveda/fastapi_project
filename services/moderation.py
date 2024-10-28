import asyncio
import os

from dotenv import load_dotenv
from google import generativeai
from google.generativeai import GenerativeModel

from comments.models import Comment
from db.database import SessionLocal

load_dotenv()

API_KEY = os.getenv("API_KEY")
generativeai.configure(api_key=API_KEY)


def is_toxic_content(text: str) -> bool:
    prompt = f"""
        Analyze the following message and determine if it contains toxic content:
        "{text}"
    
        If the content is toxic, return True. If it is not, return False.
        """

    try:
        model = generativeai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        message = response.text.lower()

        return "true" in message
    except Exception as e:
        print(f"Error analyzing content: {e}")
        return True


async def generate_auto_reply(comment_id: int) -> None:
    db = SessionLocal()
    comment = db.query(Comment).get(comment_id)
    post = comment.post

    if not post.auto_reply_enabled:
        return

    await asyncio.sleep(post.reply_delay)

    prompt = f"Generate a relevant response based on post: '{post.content}' and comment: '{comment.content}'"
    model = GenerativeModel("gemini-1.5-flash")

    try:
        response = model.generate_content(prompt)
        reply_content = response.text

        reply_comment = Comment(
            content=reply_content,
            user_id=post.user_id,
            post_id=post.id,
            is_banned=False,
        )
        db.add(reply_comment)
        db.commit()
    except Exception as e:
        print(f"Error generating reply: {e}")
    finally:
        db.close()
