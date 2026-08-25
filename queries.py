CREATE_PRODUCTS_TABLE = """
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY,
    name TEXT,
    price INTEGER
)
"""


CREATE_PRODUCT_INFO_TABLE = """
CREATE TABLE IF NOT EXISTS product_info (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER,
    category TEXT,
    description TEXT,
    FOREIGN KEY(product_id) REFERENCES products(id)
)
"""


INSERT_PRODUCT = """
INSERT INTO products (
    id,
    name,
    price
)
VALUES (?, ?, ?)
"""


INSERT_PRODUCT_INFO = """
INSERT INTO product_info (
    product_id,
    category,
    description
)
VALUES (?, ?, ?)
"""


SELECT_PRODUCTS = """
SELECT
    products.id,
    products.name,
    products.price,
    product_info.category,
    product_info.description

FROM products

INNER JOIN product_info

ON products.id = product_info.product_id
"""


SELECT_PRODUCT_BY_ID = """
SELECT
    products.id,
    products.name,
    products.price,
    product_info.category,
    product_info.description

FROM products

INNER JOIN product_info

ON products.id = product_info.product_id

WHERE products.id = ?
"""


DELETE_PRODUCT_INFO = """
DELETE FROM product_info
WHERE product_id = ?
"""


DELETE_PRODUCT = """
DELETE FROM products
WHERE id = ?
"""


# Комментарий к пункту 7:
#
# Если удалить только запись из таблицы products,
# а product_info не удалять,
# товар пропадёт из /products,
# потому что INNER JOIN не найдёт связанную запись.
#
# Но в таблице product_info останутся старые данные.
# Поэтому нужно удалять записи из обеих таблиц.
