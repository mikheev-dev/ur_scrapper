-- Extract parts-models and parts-categories relantions
-- depends: 20240127_06_iiuPE-add-parts-table

CREATE TABLE parts_models (
    part_id INTEGER REFERENCES parts(id),
    model_id INTEGER REFERENCES models(id),
    CONSTRAINT parts_models_pk PRIMARY KEY(part_id, model_id)
);

INSERT INTO parts_models(part_id, model_id)
SELECT DISTINCT part_id, model_id
FROM parts_models_categories
;

CREATE TABLE parts_categories (
    part_id INTEGER REFERENCES parts(id),
    category_id INTEGER REFERENCES categories(id),
    CONSTRAINT parts_categories_pk PRIMARY KEY(part_id, category_id)
);

INSERT INTO parts_categories
SELECT DISTINCT part_id, category_id
FROM parts_models_categories
;

DROP TABLE parts_models_categories;


