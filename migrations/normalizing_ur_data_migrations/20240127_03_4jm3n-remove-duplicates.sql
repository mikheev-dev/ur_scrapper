-- Remove duplicates
-- depends: 20240127_02_dCnnr_add_id_columns_to_tables
DELETE FROM categories
WHERE id IN
    (
        SELECT id
        FROM
            (
                SELECT
                    id,
                    ROW_NUMBER() OVER( PARTITION BY name ORDER BY id ) AS row_num
                FROM categories
            ) t
        WHERE t.row_num > 1
    );

DELETE FROM manufacturers
WHERE id IN
    (
        SELECT id
        FROM
            (
                SELECT
                    id,
                    ROW_NUMBER() OVER( PARTITION BY name ORDER BY id ) AS row_num
                FROM manufacturers
            ) t
        WHERE t.row_num > 1
    );

DELETE FROM models
WHERE id IN
    (
        SELECT id
        FROM
            (
                SELECT
                    id,
                    ROW_NUMBER() OVER( PARTITION BY name, manufacturer_name ORDER BY id ) AS row_num
                FROM models
            ) t
        WHERE t.row_num > 1
    );

DELETE FROM parts_models_categories
WHERE id IN
    (
        SELECT id
        FROM
            (
                SELECT
                    id,
                    ROW_NUMBER() OVER( PARTITION BY number, spec, model_name, category_name ORDER BY id ) AS row_num
                FROM parts_models_categories
            ) t
        WHERE t.row_num > 1
    );
