CREATE TABLE 服務分類 (
    id SERIAL PRIMARY KEY,
    分類名稱 VARCHAR(50) UNIQUE NOT NULL
);
-- 分類 項目 價格 時間
CREATE TABLE 全服務 (
    id SERIAL PRIMARY KEY,
    分類_id INTEGER REFERENCES 服務分類(id),
    項目_id INTEGER REFERENCES 服務項目(id),
    時間_id INTEGER REFERENCES 服務時間(id),
    幸福價_id INTEGER REFERENCES 服務價格(id),
    服務價_id INTEGER REFERENCES 服務價格(id),
    --服務項目名稱 VARCHAR(100) NOT NULL,
    --服務時間 INTEGER,
    --幸福價 INTEGER,
    --服務價 INTEGER,
    備註 VARCHAR(200)
);
CREATE TABLE 服務價格 (
    id SERIAL PRIMARY KEY,
    價格 VARCHAR(5) UNIQUE NOT NULL
);

CREATE TABLE 服務時間 (
    id SERIAL PRIMARY KEY,
    時間 VARCHAR(3) UNIQUE NOT NULL
);

CREATE TABLE 總服務 (
    --id SERIAL PRIMARY KEY,
    --分類_id INTEGER REFERENCES 服務分類(id),
    --分類	服務項目	服務時間 (min)	幸福價	服務價	備註
    分類 VARCHAR(10) NOT NULL,
    服務項目名稱 VARCHAR(10) NOT NULL,
    服務時間 INTEGER,
    幸福價 INTEGER,
    服務價 INTEGER,
    備註 VARCHAR(30)
);
