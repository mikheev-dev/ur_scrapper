-- Add external ids for parts table
-- depends: 20240127_04_NASP4-add-external-ids-for-manufacturers

ALTER TABLE parts_models_categories ADD COLUMN category_id INT;
ALTER TABLE parts_models_categories ADD COLUMN model_id INT;


UPDATE parts_models_categories
SET category_id = categories.id
FROM categories
WHERE categories.name = parts_models_categories.category_name;

UPDATE parts_models_categories
SET model_id = models.id
FROM models
WHERE models.name = parts_models_categories.model_name;


ALTER TABLE parts_models_categories
    ADD CONSTRAINT fk_categories
    FOREIGN KEY (category_id)
    REFERENCES categories(id);

ALTER TABLE parts_models_categories
    ADD CONSTRAINT fk_models
    FOREIGN KEY (model_id)
    REFERENCES models(id);


ALTER TABLE parts_models_categories DROP COLUMN model_name;
ALTER TABLE parts_models_categories DROP COLUMN category_name;