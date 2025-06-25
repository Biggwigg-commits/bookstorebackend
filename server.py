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
        "amazon_link": "https://www.amazon.com/BUBBLE-BEAR-MYSTERY-PUMPKIN-PIRATE/dp/B0F6YT5JRK/ref=mp_s_a_1_1?crid=1PW0GN51N523B&dib=eyJ2IjoiMSJ9.DcQo4WgnkQ64_DSrNqTu0_FfY0MithJLNs5pbKnlsHA.EhtsbaUSFbgXi3691EZifet2A52JcepMpkdmmt1JuaA&dib_tag=se&keywords=bubble+bear+and+the+mystery+of+the+pumpkin+pirate&qid=1750809695&sprefix=bubble+bear+and+the+mystery+of+the+pumpkin+pirate+%2Caps%2C152&sr=8-1",
        "featured": False
    },
    {
        "id": str(uuid.uuid4()),
        "title": "Bubble Bear and Friends Defeat Biggie the Bully",
        "author": "Garry Jordan",
        "category": "Young Readers",
        "description": "Learn about courage and friendship as Bubble Bear and friends stand up to bullying. An important story about standing up for what's right and supporting friends.",
        "price": 24.99,
        "image_url": "https://i.ibb.co/VYPTXpPm/d0c08a16-ae98-4080-af6a-0e96ba485193.jpg",
        "amazon_link": "https://www.amazon.com/BUBBLE-BEARS-GREAT-ADVENTURE-JORDAN/dp/B0BMTBF9F3/ref=mp_s_a_1_1?crid=3LCYDJ7PUTNVO&dib=eyJ2IjoiMSJ9.zMiTxvjHBD5Okjxj1WV7oHmKs9mDj1jDFhl0tlBp3_faUGF6BJELlPf2_PZuayQ6hFhLngEKslGOABLa2xgRXRGeSdu678bD4yQjFrMDywWgPz1tuu03_bJiSC9ZMz-l14uClNIg-qRDfvvodlCj18n75k_H8Rp26u-Y4QPEPY53n5Hgons7YOf6iWtocwr9VECQuF_QAX5JtJdP1PdHOA.tSnVdBVDH62wm-9xfQXDsPO_cHgJPKTQ37nl3y1bB6E&dib_tag=se&keywords=bubble+bears+great+adventure&qid=1750869871&sprefix=bubble+bears+great+adventure+%2Caps%2C175&sr=8-1",
        "featured": False
    },
    {
        "id": str(uuid.uuid4()),
        "title": "Bubble Bear and Friends Christmas",
        "author": "Garry Jordan",
        "category": "Young Readers",
        "description": "Celebrate the magic of Christmas with Bubble Bear and friends in this heartwarming holiday tale. A perfect Christmas story for young readers.",
        "price": 22.99,
        "image_url": "https://i.ibb.co/8nrLzvF3/Whats-App-Image-2025-06-25-at-6-02-11-AM.jpg",
        "amazon_link": "https://www.amazon.com/BUBBLE-FRIENDS-CHRISTMAS-GARRY-JORDAN/dp/B0F5WTHWMS/ref=mp_s_a_1_1?crid=12BVT2EI2G2XG&dib=eyJ2IjoiMSJ9.7sHz7QmP9SDRAoBGsM3OLoEQKiId3V3SyLAXAELdXTVehW61n3finAY4lgwLlgwQVyLjrFmlEH2FeQf-j3TFKIe3ZBy4iX6ys1Z-fY5XZDGsX1APF73v7lU7-KYZUo0Cv3qB_f8fHemo3M7sqWAeDhh0mdBLkCLPTI_VktvzZdEMglV-k-ZlimNFewTBTA9YtnZTzj1IikPmsLgR9XS-6A.IxPV_VU5P40N0eN4fzNGjtkNzOqRepLGM5LZSBRc1eo&dib_tag=se&keywords=bubble+bear+and+friends+Christmas&qid=1750869945&sprefix=bubble+bear+and+friends+christmas+%2Caps%2C162&sr=8-1",
        "featured": False
    },
    {
        "id": str(uuid.uuid4()),
        "title": "Little Willie Learns a Lot",
        "author": "Garry Jordan",
        "category": "Young Readers",
        "description": "An educational adventure with Little Willie as he discovers new things about the world around him. A delightful learning journey for curious young minds.",
        "price": 11.99,
        "image_url": "https://i.ibb.co/QvZ7ps9s/710decf7-f741-46a1-8557-8c6c70da4cbb.jpg",
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
        "image_url": "https://i.ibb.co/KjhqmFvT/Whats-App-Image-2025-06-25-at-6-02-12-AM-3.jpg",
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
        "price": 14.99,
        "image_url": "https://i.ibb.co/XxQpTTnn/Whats-App-Image-2025-06-25-at-7-05-03-AM.jpg",
        "amazon_link": "https://www.amazon.com/TODAY-YOU-WILL-GARRY-WIGGINS-ebook/dp/B0F3K1FP6V/ref=mp_s_a_1_1?crid=11EV9HVUL1ZN6&dib=eyJ2IjoiMSJ9.YVuMKbGX1ZD4YjHzRwerxY6Z0QNh3_CMWVteYaJMCTxf5EuWAFTBq1o4v4MRckNVi95u_SIcM7eXSjl5sLPGf8MvaZ1Br68Flibt_xuDl34W6wvUN8B026k_qvVvLWaG9N4BwjaAS3IN8HrxUXn5XCVe8N-b-kRJlhTGvCh3kpCker3T1qY3lTKSecY8ClM-4RlZsj6HmHUQGRt0A8h-uA.gGw_M1uP_fAxs5OyOJ3lRQGldaQ-_0bNsZw7wi9XkeA&dib_tag=se&keywords=today+you+will+die&qid=1750869734&sprefix=today+you+will+die+%2Caps%2C193&sr=8-1",
        "featured": True
    },
    {
        "id": str(uuid.uuid4()),
        "title": "The Midnight Heist",
        "author": "Garry Wiggins",
        "category": "Action & Thriller",
        "description": "A sophisticated crime thriller involving the perfect heist and unexpected twists. When the stakes are high, trust no one.",
        "price": 14.99,
        "image_url": "https://i.ibb.co/WvZFWsP4/Whats-App-Image-2025-06-25-at-6-02-11-AM-2.jpg",
        "amazon_link": "https://www.amazon.com/MIDNIGHT-HEIST-Mamba-GARRY-WIGGINS/dp/B0BMSKYTSS/ref=mp_s_a_1_2?crid=2SJ6UEKAK7V52&dib=eyJ2IjoiMSJ9.yo5-GNmWe7bwpDeRA_Lip7bNHpQzxc-fwo-v1QdoQxOZHiwvdvTLNdfFrVbVKNBQZa3dttudyr1QpnHwLh7FVSkWwSLO7R4zXP5uMcCsZQ_qJ-yAyIPTySG28oBqG_KJ6mRZBdsaMCoILhyL81FwNJjSqx1hJeuTEF0GbdY0QDNK1iv48oD7Xm8YeoPv8qB9iBjrOcg2hUBGd4hf5aZuXw.yuLOD_yP7uUeByDw3APJ3WIUsM3AmQ9pkNQ3QVodlm0&dib_tag=se&keywords=the+midnight+heist&qid=1750869806&sprefix=the+midnight+heist+%2Caps%2C280&sr=8-2",
        "featured": False
    },
    
    # Legal Information Category
    {
        "id": str(uuid.uuid4()),
        "title": "Beating the Feds",
        "author": "Garry Wiggins",
        "category": "Legal Information",
        "description": "Essential legal strategies and knowledge for navigating federal regulations and procedures. A comprehensive guide to understanding federal law.",
        "price": 69.00,
        "image_url": "https://i.ibb.co/KvYkBSK/Whats-App-Image-2025-06-25-at-7-10-29-AM.jpg",
        "amazon_link": "https://www.amazon.com/Beating-Feds-comprehensive-Successful-Information/dp/B0BMT22BMD/ref=mp_s_a_1_2?crid=1NEIDW5E8YN3L&dib=eyJ2IjoiMSJ9.oD0wJZ3yHoi4Vngh4Pk_KZhvvGvXWwSXoC4LnOTjbDB-VRUx_ZpLMo6rqq4MCLJSRz-RGF6MiMCc3qZFnwGKbdku5UDKbJUTpZ1sZFsC3PE.8Cbjgq_LbZmreToepf_aebMej6Z3ZZrGKrg7sL21XDE&dib_tag=se&keywords=beating+the+feds&qid=1750869667&sprefix=beating+the+feds%2Caps%2C572&sr=8-2",
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
