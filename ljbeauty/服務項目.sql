INSERT INTO 服務分類 (分類名稱) VALUES ('臉部保養');
INSERT INTO 服務分類 (分類名稱) VALUES ('芳香SPA 調理');
--然後，插入 服務項目 表的數據（假設“臉部保養”的 ID 爲 1，“芳香SPA 調理”的 ID 爲 2）：

-- 插入服務項目表數據
INSERT INTO 服務項目 (分類_id, 服務項目名稱, 服務時間, 幸福價, 服務價, 備註) 
VALUES (1, '柔嫩淨膚調理', 60, 1200, 1500, '不含粉刺調理');

INSERT INTO 服務項目 (分類_id, 服務項目名稱, 服務時間, 幸福價, 服務價, 備註) 
VALUES (1, '水漾深層調理', 90, 1600, 2000, NULL);

INSERT INTO 服務項目 (分類_id, 服務項目名稱, 服務時間, 幸福價, 服務價, 備註) 
VALUES (2, '背/腿SPA按摩', 60, 1500, 1500, NULL);

INSERT INTO 服務項目 (分類_id, 服務項目名稱, 服務時間, 幸福價, 服務價, 備註) 
VALUES (2, '浸油背景', 40, 800, 1000, NULL),
VALUES (2, '纖盈漫步', 40, 800, 1000, NULL);

INSERT INTO 服務項目 (分類_id, 服務項目名稱, 服務時間, 幸福價, 服務價, 備註) 
VALUES (2, '全身去角質', 60, 1200, 1500, '贈足浴');
