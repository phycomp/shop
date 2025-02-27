--CREATE TABLE 麗京美學 (
--    客戶 VARCHAR(255),
--    手機 VARCHAR(20),
--    生日 DATE,
--    性別 VARCHAR(10),
--    服務價格 NUMERIC(10, 2),
--    服務項目 VARCHAR(255),
--    服務時間 VARCHAR(20),
--    服務日期 DATE,
--    住址 TEXT,
--    additional_phone VARCHAR(20),
--    extra_info TEXT,
--    remarks TEXT
--);

CREATE TABLE 客戶 (
    客戶_id SERIAL PRIMARY KEY,
    姓名 VARCHAR(100) NOT NULL,
    手機 VARCHAR(15) NOT NULL,
    生日 DATE,
    性別 VARCHAR(10),
    地址 VARCHAR(255),
    備註 TEXT
);

--2. 服務表 (services):
CREATE TABLE 服務 (
    服務_id SERIAL PRIMARY KEY,
    項目 VARCHAR(100),
    名稱 VARCHAR(100) NOT NULL,
    時間 INTEGER,
    價格 DECIMAL(10, 2),
    折扣 DECIMAL(10, 2),
    備註 TEXT
);
--3. 訂單表 (orders):
CREATE TABLE 訂單 (
    訂單_id SERIAL PRIMARY KEY,
    客戶_id INT REFERENCES 客戶(customer_id),
    服務_id INT REFERENCES 服務(service_id),
    服務日期 DATE NOT NULL,
    價格 DECIMAL(10, 2)
);
