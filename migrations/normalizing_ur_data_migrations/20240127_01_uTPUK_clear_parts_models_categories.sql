-- Clear parts table
-- depends: 
DELETE FROM parts_models_categories WHERE LENGTH(number) <= 1;
DELETE FROM parts_models_categories WHERE number is NULL;