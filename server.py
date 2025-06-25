from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional
import uuid
import os
import shutil
from pymongo import MongoClient

app = FastAPI(title="Literary Depot API", version="1.0.0")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create uploads directory if it doesn't exist
os.makedirs("uploads", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# MongoDB connection
MONGO_URL = os.environ.get('MONGO_URL', 'mongodb://localhost:27017/')
client = MongoClient(MONGO_URL)
db = client.literary_depot

# Pydantic models
class Book(BaseModel):
    id: str
    title: str
    author: str
    category: str
    description: str
    price: float
    image_url: str
    amazon_link: str
    featured: bool = False

class BookCreate(BaseModel):
    title: str
    author: str
    category: str
    description: str
    price: float
    amazon_link: str
    featured: bool = False

class BookUpdate(BaseModel):
    title: Optional[str]
    author: Optional[str]
    category: Optional[str]
    description: Optional[str]
    price: Optional[float]
    amazon_link: Optional[str]
    featured: Optional[bool]

# Initialize sample data with Amazon links
sample_books = [
    # Young Readers Category
    {
        "id": str(uuid.uuid4()),
        "title": "Bubble Bears Great Adventure",
        "author": "Garry Jordan",
        "category": "Young Readers",
        "description": "Join Bubble Bear on an amazing adventure filled with friendship, discovery, and fun! A delightful story that teaches children about courage, friendship, and the joy of exploration.",
        "price": 12.99,
        "image_url": "https://i.ibb.co/ccHc420q/Whats-App-Image-2025-06-25-at-6-02-11-AM-1.jpg",
        "amazon_link": "https://www.amazon.com/dp/B08XYZ123A",
        "featured": True
    },
    {
        "id": str(uuid.uuid4()),
        "title": "Bubble Bear and Friends First Day of School",
        "author": "Garry Jordan",
        "category": "Young Readers",
        "description": "Experience the excitement and nervousness of the first day of school with Bubble Bear and friends. A heartwarming tale about new beginnings and making friends.",
        "price": 12.99,
        "image_url": "https://i.ibb.co/GvVq7Tc8/Whats-App-Image-2025-06-25-at-6-02-11-AM-3.jpg",
        "amazon_link": "https://www.amazon.com/s?k=Bubble+Bear+Friends+First+Day+School+Garry+Jordan",
        "featured": False
    },
    {
        "id": str(uuid.uuid4()),
        "title": "Bubble Bear and the Mystery of the Pumpkin Pirate",
        "author": "Garry Jordan",
        "category": "Young Readers",
        "description": "A thrilling mystery adventure as Bubble Bear solves the case of the mysterious Pumpkin Pirate. Perfect for young readers who love mysteries and adventures.",
        "price": 12.99,
        "image_url": "https://i.ibb.co/Pv0BQ11t/Whats-App-Image-2025-06-25-at-6-02-11-AM-4.jpg",
        "amazon_link": "https://www.amazon.com/s?k=Bubble+Bear+Mystery+Pumpkin+Pirate+Garry+Jordan",
        "featured": False
    },
    {
        "id": str(uuid.uuid4()),
        "title": "Bubble Bear and Friends Defeat Biggie the Bully",
        "author": "Garry Jordan",
        "category": "Young Readers",
        "description": "Learn about courage and friendship as Bubble Bear and friends stand up to bullying. An important story about standing up for what's right and supporting friends.",
        "price": 12.99,
        "image_url": "https://images.unsplash.com/photo-1481627834876-b7833e8f5570",
        "amazon_link": "https://www.amazon.com/s?k=Bubble+Bear+Friends+Defeat+Biggie+Bully+Garry+Jordan",
        "featured": False
    },
    {
        "id": str(uuid.uuid4()),
        "title": "Bubble Bear and Friends Christmas",
        "author": "Garry Jordan",
        "category": "Young Readers",
        "description": "Celebrate the magic of Christmas with Bubble Bear and friends in this heartwarming holiday tale. A perfect Christmas story for young readers.",
        "price": 12.99,
        "image_url": "https://i.ibb.co/8nrLzvF3/Whats-App-Image-2025-06-25-at-6-02-11-AM.jpg",
        "amazon_link": "https://www.amazon.com/s?k=Bubble+Bear+Friends+Christmas+Garry+Jordan",
        "featured": False
    },
    {
        "id": str(uuid.uuid4()),
        "title": "Little Willie Learns a Lot",
        "author": "Garry Jordan",
        "category": "Young Readers",
        "description": "An educational adventure with Little Willie as he discovers new things about the world around him. A delightful learning journey for curious young minds.",
        "price": 11.99,
        "image_url": "https://images.unsplash.com/photo-1503676260728-1c00da094a0b",
        "amazon_link": "https://www.amazon.com/s?k=Little+Willie+Learns+Lot+Garry+Jordan",
        "featured": False
    },
    
    # Business & Self-Help Category
    {
        "id": str(uuid.uuid4()),
        "title": "Think Rich and Grow Rich",
        "author": "Garry Jordan",
        "category": "Business & Self-Help",
        "description": "Unlock the secrets to building wealth and achieving financial success through proven strategies and timeless principles that have helped countless individuals achieve prosperity.",
        "price": 24.99,
        "image_url": "https://i.ibb.co/TMSQVDWc/Whats-App-Image-2025-06-25-at-6-02-12-AM.jpg",
        "amazon_link": "https://www.amazon.com/Think-Grow-Rich-Landmark-Bestseller/dp/1585424331",
        "featured": True
    },
    {
        "id": str(uuid.uuid4()),
        "title": "100 Side Hustles That Will Make You a Millionaire",
        "author": "Garry Wiggins",
        "category": "Business & Self-Help",
        "description": "Discover 100 proven side hustles and business ideas that can transform your financial future. From digital marketing to real estate, find the perfect opportunity for you.",
        "price": 19.99,
        "image_url": "https://i.ibb.co/8g6NMs89/Whats-App-Image-2025-06-25-at-6-02-12-AM-2.jpg",
        "amazon_link": "https://www.amazon.com/s?k=100+Side+Hustles+Millionaire+Garry+Wiggins",
        "featured": False
    },
    {
        "id": str(uuid.uuid4()),
        "title": "What the Billionaires Won't Tell You",
        "author": "Garry Jordan",
        "category": "Business & Self-Help",
        "description": "Insider secrets and strategies from the world's wealthiest individuals. Learn the mindset and tactics that separate the ultra-wealthy from everyone else.",
        "price": 22.99,
        "image_url": "https://i.ibb.co/fzR440YM/Whats-App-Image-2025-06-25-at-6-02-12-AM-1.jpg",
        "amazon_link": "https://www.amazon.com/s?k=What+Billionaires+Won't+Tell+You+Garry+Jordan",
        "featured": False
    },
    {
        "id": str(uuid.uuid4()),
        "title": "The AI Millionaire",
        "author": "Dr. Orion Vexel",
        "category": "Business & Self-Help",
        "description": "Harness the power of artificial intelligence to build wealth in the digital age. Learn cutting-edge strategies for leveraging AI in business and investments.",
        "price": 29.99,
        "image_url": "https://i.ibb.co/4Z5cv9rV/1a7d4246-702f-488f-bd88-4761f0f37e10.jpg",
        "amazon_link": "https://www.amazon.com/AI-MILLIONAIRE-Fortune-Automated-Intelligence/dp/B0F2XRJJKL/ref=mp_s_a_1_1?dib=eyJ2IjoiMSJ9.xy_6XUK1rjM43C7QFi-2rg.f5Y8Vnx7rHhG6lKDb0GREQmBFxJDOmQYkvr3luYFhP8&dib_tag=se&keywords=AI+Millionaire+Dr+Orion+Vexel&qid=1750783916&sr=8-1",
        "featured": True
    },
    {
        "id": str(uuid.uuid4()),
        "title": "The Art of Hustling",
        "author": "Garry Wiggins",
        "category": "Business & Self-Help",
        "description": "Master the mindset and skills needed to succeed in any entrepreneurial venture. Learn the art of turning opportunities into profitable businesses.",
        "price": 18.99,
        "image_url": "https://i.ibb.co/XxF42Xmm/Whats-App-Image-2025-06-25-at-6-58-45-AM.jpg",
        "amazon_link": "https://www.amazon.com/s?k=Art+of+Hustling+Garry+Wiggins",
        "featured": False
    },
    {
        "id": str(uuid.uuid4()),
        "title": "The Secrets of Getting Rich",
        "author": "Preston Rockefeller",
        "category": "Business & Self-Help",
        "description": "Time-tested principles and strategies for building lasting wealth from one of America's most prominent financial families.",
        "price": 21.99,
        "image_url": "https://i.ibb.co/KjhqmFvT/Whats-App-Image-2025-06-25-at-6-02-12-AM-3.jpg",
        "amazon_link": "https://www.amazon.com/s?k=Secrets+Getting+Rich+Preston+Rockefeller",
        "featured": False
    },
    {
        "id": str(uuid.uuid4()),
        "title": "What the Rich Won't Tell You",
        "author": "Preston Rockefeller",
        "category": "Business & Self-Help",
        "description": "Exclusive insights from generational wealth builders and their proven strategies. Learn the secrets that have been passed down through wealthy families for generations.",
        "price": 26.99,
        "image_url": "https://images.unsplash.com/photo-1434626881859-194d67b2b86f",
        "amazon_link": "https://www.amazon.com/s?k=What+Rich+Won't+Tell+You+Preston+Rockefeller",
        "featured": False
    },
    
    # Action & Thriller Category
    {
        "id": str(uuid.uuid4()),
        "title": "Today You Will Die",
        "author": "Garry Wiggins",
        "category": "Action & Thriller",
        "description": "A heart-pounding thriller that will keep you on the edge of your seat until the very last page. When death comes calling, every second counts.",
        "price": 16.99,
        "image_url": "https://i.ibb.co/XxQpTTnn/Whats-App-Image-2025-06-25-at-7-05-03-AM.jpg",
        "amazon_link": "https://www.amazon.com/s?k=Today+You+Will+Die+Garry+Wiggins",
        "featured": True
    },
    {
        "id": str(uuid.uuid4()),
        "title": "The Midnight Heist",
        "author": "Garry Wiggins",
        "category": "Action & Thriller",
        "description": "A sophisticated crime thriller involving the perfect heist and unexpected twists. When the stakes are high, trust no one.",
        "price": 17.99,
        "image_url": "https://i.ibb.co/WvZFWsP4/Whats-App-Image-2025-06-25-at-6-02-11-AM-2.jpg",
        "amazon_link": "https://www.amazon.com/s?k=Midnight+Heist+Garry+Wiggins",
        "featured": False
    },
    
    # Legal Information Category
    {
        "id": str(uuid.uuid4()),
        "title": "Beating the Feds",
        "author": "Garry Wiggins",
        "category": "Legal Information",
        "description": "Essential legal strategies and knowledge for navigating federal regulations and procedures. A comprehensive guide to understanding federal law.",
        "price": 34.99,
        "image_url": "https://i.ibb.co/KvYkBSK/Whats-App-Image-2025-06-25-at-7-10-29-AM.jpg",
        "amazon_link": "https://www.amazon.com/s?k=Beating+the+Feds+Garry+Wiggins",
        "featured": False
    },
    {
        "id": str(uuid.uuid4()),
        "title": "Beating the Feds II",
        "author": "Garry Wiggins",
        "category": "Legal Information",
        "description": "Advanced legal strategies and updated information for federal case management. The sequel to the bestselling legal guide.",
        "price": 36.99,
        "image_url": "https://i.ibb.co/P2k1zq3/Whats-App-Image-2025-06-25-at-6-02-11-AM-5.jpg",
        "amazon_link": "https://www.amazon.com/s?k=Beating+the+Feds+II+Garry+Wiggins",
        "featured": False
    }
]

@app.on_event("startup")
async def startup_event():
    # Clear existing data and insert sample books
    db.books.delete_many({})
    db.books.insert_many(sample_books)
    print("Sample books inserted successfully!")

@app.get("/api/books", response_model=List[Book])
async def get_books(category: Optional[str] = None, featured: Optional[bool] = None):
    """Get all books or filter by category/featured status"""
    query = {}
    if category:
        query["category"] = category
    if featured is not None:
        query["featured"] = featured
    
    books = list(db.books.find(query, {"_id": 0}))
    return books

@app.get("/api/books/{book_id}", response_model=Book)
async def get_book(book_id: str):
    """Get a specific book by ID"""
    book = db.books.find_one({"id": book_id}, {"_id": 0})
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@app.get("/api/categories")
async def get_categories():
    """Get all book categories"""
    categories = db.books.distinct("category")
    return {"categories": categories}

@app.get("/api/featured-books", response_model=List[Book])
async def get_featured_books():
    """Get featured books"""
    books = list(db.books.find({"featured": True}, {"_id": 0}))
    return books

@app.post("/api/books", response_model=Book)
async def create_book(book: BookCreate):
    """Create a new book"""
    book_dict = book.dict()
    book_dict["id"] = str(uuid.uuid4())
    book_dict["image_url"] = "https://images.unsplash.com/photo-1544947950-fa07a98d237f"  # Default image
    
    db.books.insert_one(book_dict)
    return book_dict

@app.put("/api/books/{book_id}", response_model=Book)
async def update_book(book_id: str, book_update: BookUpdate):
    """Update a book"""
    book = db.books.find_one({"id": book_id})
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    update_data = {k: v for k, v in book_update.dict().items() if v is not None}
    if update_data:
        db.books.update_one({"id": book_id}, {"$set": update_data})
    
    updated_book = db.books.find_one({"id": book_id}, {"_id": 0})
    return updated_book

@app.post("/api/books/{book_id}/upload-cover")
async def upload_book_cover(book_id: str, file: UploadFile = File(...)):
    """Upload a book cover image"""
    book = db.books.find_one({"id": book_id})
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    # Save the uploaded file
    file_extension = file.filename.split(".")[-1]
    filename = f"{book_id}.{file_extension}"
    file_path = f"uploads/{filename}"
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Update book image URL
    image_url = f"/uploads/{filename}"
    db.books.update_one({"id": book_id}, {"$set": {"image_url": image_url}})
    
    return {"message": "Cover uploaded successfully", "image_url": image_url}

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "message": "Literary Depot API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
