from fastapi import FastAPI
from routers import user, flight, notification
from utils.database import engine, Base
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

# Initialize FastAPI app
app = FastAPI()

# Add CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Include routers
# app.include_router(user.router, prefix="/users", tags=["Users"])
app.include_router(flight.router, prefix="/flights", tags=["Flights"])
app.include_router(notification.router, prefix="/notifications", tags=["Notification"])

# Create database tables
Base.metadata.create_all(bind=engine)

# Run the server using uvicorn if this file is executed directly
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
