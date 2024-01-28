-- Add external ids for tables
-- depends: 20240127_03_4jm3n-remove-duplicates
ALTER TABLE models ADD COLUMN manufacturer_id INT;

UPDATE models
SET manufacturer_id = manufacturers.id
FROM manufacturers
WHERE manufacturers.name = models.manufacturer_name;

ALTER TABLE models
    ADD CONSTRAINT fk_manufacturers
    FOREIGN KEY (manufacturer_id)
    REFERENCES manufacturers(id);

ALTER TABLE models DROP COLUMN manufacturer_name;
