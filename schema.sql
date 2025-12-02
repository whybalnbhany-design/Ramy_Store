DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS product;
DROP TABLE IF EXISTS cart_item;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE products (
    product_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    name         TEXT    NOT NULL,
    price        REAL    NOT NULL,
    image_url    TEXT    NOT NULL,
    category     TEXT    NOT NULL,
    details      TEXT
);

CREATE TABLE cart_items (
    cart_item_id  INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id       INTEGER    NOT NULL,
    product_id    INTEGER    NOT NULL,
    quantity      INTEGER    NOT NULL DEFAULT 1,
    added_at      TIMESTAMP   NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user(id),
    FOREIGN KEY (product_id) REFERENCES product(product_id)
);
