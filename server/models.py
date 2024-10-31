from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators 
    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError('You must enter a name.')
        
        author = Author.query.filter_by(name=name).first()
        if author:
            raise ValueError('You must enter a unique name.')
        
        return name
    
    @validates('phone_number')
    def validate_phone_number(self, key, number):
        if len(number) != 10 or not number.isdigit():
            raise ValueError('You must enter a ten digit number.')
        
        return number

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators  

    @validates('title')
    def validate_title(self, key, title):
        if not title:
            raise ValueError('Post must have a title.')
        
        buzzwords = ["Won't Believe", "Secret", "Top", "Guess"]
        if not any(word in title for word in buzzwords):
            raise ValueError('Title is not clickbait-y enough!')
        
        return title

    @validates('content')
    def validate_content(self, key, content):
        if len(content) < 250:
            raise ValueError('Content must be at least 250 characters')
        
        return content
    
    @validates('summary')
    def validate_summary(self, key, summary):
        if len(summary) > 250:
            raise ValueError('Summary may not exceed 250 characters.')
        
        return summary
    
    @validates('category')
    def validate_category(self, key, category):
        if category not in ['Fiction', 'Non-Fiction']:
            raise ValueError('Category must be fiction or non-fiction.')
        
        return category

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
