-- 1) Таблица rooms_room
CREATE TABLE IF NOT EXISTS public.rooms_room (
    id SERIAL PRIMARY KEY,
    number VARCHAR(10) NOT NULL UNIQUE,
    room_type VARCHAR(50) NOT NULL,
    price_per_night NUMERIC(8, 2) NOT NULL,
    capacity INTEGER NOT NULL,
    description TEXT
);

-- 2) Таблица bookings_booking
CREATE TABLE IF NOT EXISTS public.bookings_booking (
    id SERIAL PRIMARY KEY,
    room_id INTEGER NOT NULL REFERENCES public.rooms_room(id) ON DELETE CASCADE,
    guest_name VARCHAR(100) NOT NULL,
    check_in DATE NOT NULL,
    check_out DATE NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'pending',
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);
