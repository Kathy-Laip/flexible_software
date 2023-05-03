create or replace function DELETE_PRODUCTS_CATEGORY_ON_PRODUCT_DELETE_BEFORE()
returns trigger
language 'plpgsql'
as
$$
begin
    delete from products_to_buy as buys where buys."product_ID"=OLD.id;
    return OLD;
end;
$$

create or replace function DELETE_PRODUCTS_CATEGORY_ON_PRODUCT_DELETE_AFTER()
returns trigger
language 'plpgsql'
as
$$
begin
    delete from products_categories as cats where cats.id=OLD.category;
    return OLD;
end;
$$

CREATE TRIGGER DELETE_PRODUCTS_CATEGORY_ON_PRODUCT_DELETE_BEFORE_TRIGGER before delete
on "products" for each row
execute function DELETE_PRODUCTS_CATEGORY_ON_PRODUCT_DELETE_BEFORE();

CREATE TRIGGER DELETE_PRODUCTS_CATEGORY_ON_PRODUCT_DELETE_AFTER_TRIGGER after delete
on "products" for each row
execute function DELETE_PRODUCTS_CATEGORY_ON_PRODUCT_DELETE_AFTER();