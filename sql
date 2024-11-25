CREATE TABLE States (
    state_id SERIAL PRIMARY KEY,
    icao24 VARCHAR(10),            -- Aircraft identifier
    callsign VARCHAR(8),           -- Flight number or callsign
    origin_country VARCHAR(50),    -- Country of origin
    latitude NUMERIC,              -- Current latitude
    longitude NUMERIC,             -- Current longitude
    baro_altitude NUMERIC,         -- Barometric altitude
    geo_altitude NUMERIC,          -- Geometric altitude
    velocity NUMERIC,              -- Speed in m/s
    true_track NUMERIC,            -- Direction of travel
    vertical_rate NUMERIC,         -- Climb or descent rate
    on_ground BOOLEAN,             -- True if the aircraft is on the ground
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Time of the record
);


CREATE TABLE FlightsAll (
    flight_id SERIAL PRIMARY KEY,
    icao24 VARCHAR(10),            -- Aircraft identifier
    callsign VARCHAR(8),           -- Flight number or callsign
    departure_airport VARCHAR(10), -- IATA/ICAO code of departure airport
    arrival_airport VARCHAR(10),   -- IATA/ICAO code of arrival airport
    departure_time TIMESTAMP,      -- Time of departure
    arrival_time TIMESTAMP,        -- Time of arrival
);
