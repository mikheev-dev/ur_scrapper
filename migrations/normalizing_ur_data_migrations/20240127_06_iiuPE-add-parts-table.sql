-- Add models-parts m2m table
-- depends: 20240127_05_s3LLs-add-external-ids-for-parts-models-categories
--
--
CREATE TABLE parts (
	number VARCHAR(50),
	spec VARCHAR(200),
	id SERIAL PRIMARY KEY
);

INSERT INTO parts(number, spec)
SELECT DISTINCT
    number, spec
FROM parts_models_categories
;

ALTER TABLE parts_models_categories DROP COLUMN spec;
ALTER TABLE parts_models_categories ADD COLUMN part_id INT;

UPDATE parts_models_categories
SET part_id = parts.id
FROM parts
WHERE parts.number = parts_models_categories.number;

ALTER TABLE parts_models_categories DROP COLUMN number;
ALTER TABLE parts_models_categories DROP COLUMN id;

