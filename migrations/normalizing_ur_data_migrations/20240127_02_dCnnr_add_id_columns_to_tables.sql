-- Add id columns to tables
-- depends: 20240127_01_uTPUK_clear_parts_models_categories
ALTER TABLE manufacturers ADD COLUMN id SERIAL PRIMARY KEY;
ALTER TABLE categories ADD COLUMN id SERIAL PRIMARY KEY;
ALTER TABLE models  ADD COLUMN id SERIAL PRIMARY KEY;
ALTER TABLE parts_models_categories ADD COLUMN id SERIAL;

