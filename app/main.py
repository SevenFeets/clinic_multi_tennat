"""
Main FastAPI application entry point

🎯 YOUR MISSION (Week 1):
1. Create a FastAPI application instance
2. Add a health check endpoint
3. Add CORS middleware (allows frontend to connect)
4. Run the server and visit http://localhost:8000/docs

📚 LEARNING RESOURCES:
- FastAPI First Steps: https://fastapi.tiangolo.com/tutorial/first-steps/
- Python async/await: https://realpython.com/async-io-python/

💡 HINTS:
- FastAPI is imported from the fastapi package
- Use @app.get() decorator for GET endpoints
- All endpoint functions should be async (use 'async def')
- Return a dictionary from endpoints - FastAPI converts it to JSON automatically
"""

# TODO: Import FastAPI
from fastapi import FastAPI

# TODO: Import CORS middleware
from fastapi.middleware.cors import CORSMiddleware

# TODO: Create FastAPI app instance
app = FastAPI(title="Clinic Management API", version="1.0.0")

# TODO: Add CORS middleware (allows frontend to call your API)
# HINT: Look up "FastAPI CORS" - you need to add_middleware with CORSMiddleware
# HINT: For development, you can allow all origins with ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True, 
    allow_methods=["*"], 
    allow_headers=["*"],
)


# TODO: Create a health check endpoint
# HINT: Use @app.get("/health")
# HINT: Return something like {"status": "healthy", "message": "API is running"}
@app.get("/health") 
async def health_check():
    return {"status": "healthy", "message": "API is running"}

# TODO: Create a welcome endpoint at "/"
# HINT: Return a friendly welcome message with API info
@app.get("/")
async def main():
    return {"message": "Welcome to the Clinic Management API"}


from datetime import datetime
@app.get("/datetime")
async def get_datetime():
    return {"datetime": str(datetime.now())}


@app.get("/about")
async def about():
    return {"message": "This is the about page"}

@app.get("/contact")
async def contact():
    return {"message": "This is the contact page"}

@app.get("/services")
async def services():
    return {"message": "This is the services page"}

@app.get("/products")
async def products():
    return {"message": "This is the products page"}

# 🧪 TESTING YOUR WORK:
# 1. Run: uvicorn app.main:app --reload
# 2. Visit: http://localhost:8000/docs
# 3. Try out your endpoints in the interactive documentation!
# 4. You should see your endpoints listed and be able to test them

