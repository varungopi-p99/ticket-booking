from fastapi import FastAPI
from app.db.database import Base, engine
from app.routers import auth, movie_routes, showtime_routes, seat_routes, admin_routes, booking_routes
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Movie Ticket Booking System")

Base.metadata.create_all(bind=engine)

origins = [
    "http://52.200.176.69",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.add.middleware(
#     TrustedHostMiddleware,
#     allowed_host=["*", ]
# )

app.include_router(auth.router)
app.include_router(movie_routes.router)
app.include_router(showtime_routes.router)
app.include_router(seat_routes.router)
app.include_router(booking_routes.router)
app.include_router(admin_routes.router)
# app.include_router(payment_routes.router)

@app.get("/")
async def root():
    return {"message": "ticket booking system"}

