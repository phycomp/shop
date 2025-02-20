以下是為宗教云商城設計的 PostgreSQL 數據庫 Schema，采用模塊化設計支持多類型商品/服務管理，包含詳細注釋與宗教特色字段：

```sql
-------------------
-- 核心用戶系統 --
-------------------
CREATE TABLE users (
    user_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    avatar_url TEXT,
    membership_level VARCHAR(20) DEFAULT '普通' 
      CHECK (membership_level IN ('普通', '信徒', '法師')),
    karma_points INT DEFAULT 0 CHECK (karma_points >= 0),
    fu_coins DECIMAL(10,2) DEFAULT 0.00 CHECK (fu_coins >= 0),
    religious_cert JSONB, -- 存儲皈依證/法會認證等宗教身份信息
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

COMMENT ON TABLE users IS '用戶主表，包含宗教認證狀態與數字資產';
COMMENT ON COLUMN users.religious_cert IS '存儲加密後的宗教身份認證數據';

-------------------
-- 商品服務體系 --
-------------------
CREATE TABLE listings (
    item_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(user_id),
    item_type VARCHAR(20) NOT NULL 
      CHECK (item_type IN ('physical', 'service', 'digital', 'handmade')),
    category VARCHAR(50) NOT NULL 
      CHECK (category IN ('法物', '經書', '念珠', '唐卡', '法會服務', '修行用品')),
    title VARCHAR(100) NOT NULL,
    description TEXT,
    attributes JSONB NOT NULL, -- 類型專用屬性
    price DECIMAL(10,2) CHECK (price >= 0),
    karma_price INT, -- 功德點兌換價
    status VARCHAR(20) DEFAULT 'draft' 
      CHECK (status IN ('draft', 'pending', 'approved', 'rejected')),
    audit_trail JSONB[], -- 審核記錄
    blessing_info JSONB, -- 開光信息
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

COMMENT ON TABLE listings IS '統一商品/服務列表';
COMMENT ON COLUMN listings.attributes IS '動態屬性，例：法物={材質,尺寸}, 服務={時長,地點}';
COMMENT ON COLUMN listings.blessing_info IS '包含開光法師、日期、寺院信息';

-- 宗教特色枚舉類型
CREATE TYPE dharma_service_type AS ENUM (
    '共修活動', '法器維護', '法會義工', '經書抄寫', '齋食供應'
);

CREATE TABLE services (
    service_id UUID PRIMARY KEY REFERENCES listings(item_id),
    service_type dharma_service_type NOT NULL,
    location GEOGRAPHY(Point,4326), -- 服務地點坐標
    duration INTERVAL,
    max_participants INT
);

COMMENT ON TABLE services IS '宗教服務擴展信息';

-------------------
-- 交易管理系統 --
-------------------
CREATE TABLE orders (
    order_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(user_id),
    total_amount DECIMAL(10,2) NOT NULL,
    payment_method VARCHAR(20) 
      CHECK (payment_method IN ('paypal', 'karma', 'fu', 'mixed')),
    karma_used INT DEFAULT 0,
    fu_used DECIMAL(10,2) DEFAULT 0,
    coupon_used VARCHAR(20),
    order_status VARCHAR(20) DEFAULT 'pending'
      CHECK (order_status IN ('pending', 'paid', 'shipped', 'completed')),
    dharma_notes TEXT, -- 宗教需求備注
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE order_items (
    order_item_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_id UUID REFERENCES orders(order_id),
    item_id UUID REFERENCES listings(item_id),
    quantity INT NOT NULL CHECK (quantity > 0),
    is_service BOOLEAN NOT NULL
);

COMMENT ON COLUMN orders.dharma_notes IS '可存放供佛要求、回向文等宗教信息';

-------------------
-- 宗教審核系統 --
-------------------
CREATE TABLE audits (
    audit_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    item_id UUID REFERENCES listings(item_id),
    auditor_id UUID REFERENCES users(user_id),
    audit_type VARCHAR(20) NOT NULL
      CHECK (audit_type IN ('initial', 'appeal', 'periodic')),
    result VARCHAR(10) NOT NULL CHECK (result IN ('approved', 'rejected')),
    comments TEXT,
    rule_violations JSONB, -- 違規條目記錄
    created_at TIMESTAMPTZ DEFAULT NOW()
);

COMMENT ON TABLE audits IS '包含AI審核與人工審核記錄';
COMMENT ON COLUMN audits.rule_violations IS '存儲觸發的具體審核規則條目';

-------------------
-- 優惠系統 --
-------------------
CREATE TABLE coupons (
    coupon_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    code VARCHAR(20) UNIQUE NOT NULL,
    discount_type VARCHAR(10) CHECK (discount_type IN ('percent', 'fixed')),
    value DECIMAL(10,2) NOT NULL,
    min_order DECIMAL(10,2) DEFAULT 0,
    applicable_to JSONB, -- 適用商品類別
    valid_from DATE NOT NULL,
    valid_until DATE NOT NULL,
    religious_restriction BOOLEAN DEFAULT FALSE -- 信徒專屬
);

-------------------
-- 索引優化 --
-------------------
CREATE INDEX idx_listings_category ON listings USING gin(category);
CREATE INDEX idx_services_location ON services USING gist(location);
CREATE INDEX idx_users_karma ON users(karma_points);

-- 分區表示例（按年分區的交易記錄）
CREATE TABLE transactions_2023 PARTITION OF transactions
    FOR VALUES FROM ('2023-01-01') TO ('2024-01-01');
```

### 架構特點說明：

1. **宗教融合設計**
- 專屬宗教商品分類（法物/唐卡/念珠）
- 服務類型包含法會義工/共修活動等宗教特色
- 訂單備注欄位存放回向文等宗教信息

2. **靈活擴展機制**
- 使用JSONB字段存儲動態屬性
- 地理位置支持GIS查詢
- 通用`listings`表通過`item_type`區分子類型

3. **安全合規措施**
- 審核系統記錄完整審計軌迹
- 宗教認證信息加密存儲
- 分區表提升交易記錄查詢效率

4. **功德經濟整合**
- 支持功德點與法幣混合支付
- 商品可設置雙重定價（法幣+功德點）
- 信徒專屬優惠券標識

### 示例查詢：查找附近可用的法會義工服務
```sql
SELECT s.*, ST_Distance(location, ST_MakePoint(121.5,25.0)) as distance
FROM services s
JOIN listings l ON s.service_id = l.item_id
WHERE l.category = '法會服務'
  AND l.status = 'approved'
  AND ST_DWithin(location, ST_MakePoint(121.5,25.0)::geography, 5000)
ORDER BY distance;
```

此 Schema 設計滿足以下宗教電商需求：
1. 支持實體商品與宗教服務混合銷售
2. 功德點與法幣復合支付系統
3. 宗教敏感商品審核機制
4. 信徒會員專屬功能擴展
5. 法物開光信息追溯
6. 宗教活動地理位置服務

建議配合 PostgreSQL 擴展模塊：
- PostGIS：空間數據查詢
- pgcrypto：敏感數據加密
- pg_partman：分區表管理
- pg_trgm：全文檢索優化
