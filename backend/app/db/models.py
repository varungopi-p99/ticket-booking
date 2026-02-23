from sqlalchemy import Column, Integer, String, Boolean, Text, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.db.database import Base
import enum

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=True)
    phone = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, default="user")

    bookings = relationship("Booking", back_populates="user")


class Theatre(Base):
    __tablename__ = "theatres"

    id = Column(Integer, primary_key=True, index=True)
    theatre_name = Column(String, nullable=False)
    loc_name = Column(String, nullable=False)

    showtimes = relationship("Showtime", back_populates="theatre")

class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True, nullable=True)
    description = Column(Text, nullable=True)
    duration = Column(Integer, nullable=False)  # in minutes
    release_date = Column(DateTime, default=datetime.now(timezone.utc))
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    image_url = Column(String(500), nullable=True)

    showtimes = relationship("Showtime", back_populates="movie")

class Showtime(Base):
    __tablename__ = "showtimes"

    id = Column(Integer, primary_key=True, index=True)
    movie_id = Column(Integer, ForeignKey("movies.id"), nullable=False)
    theatre_id = Column(Integer, ForeignKey("theatres.id"), nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)

    movie = relationship("Movie", back_populates="showtimes")
    theatre = relationship("Theatre", back_populates="showtimes")
    seats = relationship("Seat", back_populates="showtime")

class SeatStatus(str, enum.Enum):
    AVAILABLE = "available"
    BOOKED = "booked"
    RESERVED = "reserved"

class Seat(Base):
    __tablename__ = "seats"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    showtime_id = Column(Integer, ForeignKey("showtimes.id"), nullable=False)
    row = Column(String(5), nullable=False)
    col = Column(Integer, nullable=False)
    seat_number = Column(String(10), nullable=False)
    status = Column(Enum(SeatStatus), default=SeatStatus.AVAILABLE, nullable=False)

    showtime = relationship("Showtime", back_populates="seats")
    booking = relationship("Booking", back_populates="seat")
 
class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    seat_id = Column(Integer, ForeignKey("seats.id"), nullable=False)
    booked_at = Column(DateTime, default=datetime.now(timezone.utc))
    payment_status = Column(String, nullable=False)
    payment_amount = Column(Integer, nullable=False)

    user = relationship("User", back_populates="bookings")
    seat = relationship("Seat", back_populates="booking")