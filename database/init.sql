CREATE EXTENSION IF NOT EXISTS postgis;

CREATE TABLE restaurants (
    id SERIAL PRIMARY KEY,
    name TEXT,
    category TEXT,
    description TEXT,
    location GEOGRAPHY(Point, 4326)
);

INSERT INTO restaurants (name, category, description, location) VALUES
('CELIETI', 'Panaderia', 'Gluten Free', ST_GeogFromText('POINT(-90.51522 14.58236)')),
('Wild', 'Restaurante', 'Opciones Gluten Free', ST_GeogFromText('POINT(-90.48611 14.61031)')),
('Contour Lines Center', 'Cafeteria', 'Gluten Free', ST_GeogFromText('POINT(-90.78118 14.54834)')),
('GIANNI''S La Noria', 'Restaurante', 'Opciones Gluten Free', ST_GeogFromText('POINT(-90.54568 14.58213)')),
('El Mercadito de Lola', 'Cafeteria', 'Gluten Free', ST_GeogFromText('POINT(-90.48546 14.58686)'));