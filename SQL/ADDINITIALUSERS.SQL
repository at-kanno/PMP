CREATE TABLE IF NOT EXISTS USER_TABLE
      (user_id INTEGER PRIMARY KEY,
      lastname TEXT, firstname TEXT, lastyomi TEXT, firstyomi TEXT,
      tel1 TEXT, tel2 TEXT, tel3 TEXT, zip1 TEXT, zip2 TEXT,
      company TEXT, department TEXT, prefecture INTEGER, city TEXT,
      town TEXT, building TEXT, mail_adr TEXT, status INTEGER,
      password TEXT, stage INTEGER);

INSERT INTO USER_TABLE (user_id, lastname, firstname, lastyomi, firstyomi,
tel1, tel2, tel3, zip1, zip2, company, department, prefecture, city, town, building,
status, password, mail_adr) VALUES
(1, "官野", "あつし", "かんの", "あつし", "048", "235", "4486", "351", "0035", "オリーブネット株式会社",
 "代表鳥取締役", 23, "朝霞市", "朝志ヶ丘", "朝志ヶ丘ビルディング", 3, "aaa", "kanno@olivenet.co.jp" );
INSERT INTO USER_TABLE (user_id, lastname, firstname, lastyomi, firstyomi,
tel1, tel2, tel3, zip1, zip2, company, department, prefecture, city, town, building,
status, password, mail_adr) VALUES
(2, "荒川", "幸式", "あらかわ", "ゆきのり", "03", "5577", "5311", "113", "0033", "株式会社アーク",
 "代表鳥取締役", 26, "文京区", "本郷５丁目３３番１０号", "いちご本郷ビル５階", 3, "arakawa", "ark@email.co.jp" );
INSERT INTO USER_TABLE (user_id, lastname, firstname, lastyomi, firstyomi,
tel1, tel2, tel3, zip1, zip2, company, department, prefecture, city, town, building,
status, password, mail_adr) VALUES
(3, "宮内", "綾", "みやうち", "あや", "03", "5577", "5311", "113", "0033", "株式会社アーク",
 "総務部長", 26, "文京区", "本郷５丁目３３番１０号", "いちご本郷ビル５階", 3, "miyauchi", "miyauchi.ark@gmail.com" );
INSERT INTO USER_TABLE (user_id, lastname, firstname, lastyomi, firstyomi,
tel1, tel2, tel3, zip1, zip2, company, department, prefecture, city, town, building,
status, password, mail_adr) VALUES
(4, "小岩", "貞美", "こいわ", "さだよし", "03", "5577", "5311", "112", "0002", "株式会社アーク",
 "講師", 26, "文京区", "小石川１丁目13番12号", "WAKOU小石川ビル４階", 3, "koiwa", "koiwa@mail.co.jp" );
INSERT INTO USER_TABLE (user_id, lastname, firstname, lastyomi, firstyomi,
tel1, tel2, tel3, zip1, zip2, company, department, prefecture, city, town, building,
status, password, mail_adr) VALUES
(5, "メール", "送信者", "メール", "そうしん", "048", "235", "4486", "351", "0035", "オリーブネット株式会社",
 "CIO", "埼玉県", "朝霞市", "朝志ヶ丘", "朝志ヶ丘ビルディング", 3, "ArkOliveNet2022", "itil4exercise@gmail.com" );

UPDATE USER_TABLE SET PASSWORD = 'V+KzypVRAqRVKVnEUjIaE2uDCyRLdcMH+3N33/8o5R6+K3uW9AUicrOsJXrZH3oU' where user_id=1;
UPDATE USER_TABLE SET PASSWORD = 'Sq9yEWpL2DGNSlD9CygxBhPc0k06GyaUm02GF9QgOxzpJVEhlsiasC9Df64T5Tj3' where user_id=2;
UPDATE USER_TABLE SET PASSWORD = 'WzUuwNOg9jUy2tH3hHd9MgRyLKC1Ww3YPZrWutbbafux+iwC+/OH77O7vz992Lvt' where user_id=3;
UPDATE USER_TABLE SET PASSWORD = 'oT3cgyD7kTshEED+KPCYJQpABeSIuT867tk4U4twU+2lKMtzprZkNF7xU2yN41Oe' where user_id=4;

INSERT INTO USER_TABLE (user_id, lastname, firstname, lastyomi, firstyomi,
tel1, tel2, tel3, zip1, zip2, company, department, prefecture, city, town, building,
status, password, mail_adr) VALUES
(11, "鈴木", "一郎", "すずき", "イチロウ", "090", "1234", "5678", "100", "0035", "オリーブネット株式会社",
 "営業部", 23, "朝霞市", "朝志ヶ丘", "朝志ヶ丘ビルディング", 3, "OliveNet", "user1@gmail.com" );
INSERT INTO USER_TABLE (user_id, lastname, firstname, lastyomi, firstyomi,
tel1, tel2, tel3, zip1, zip2, company, department, prefecture, city, town, building,
status, password, mail_adr) VALUES
(12, "鈴木", "次郎", "すずき", "ジロウ", "090", "1234", "5678", "100", "0035", "オリーブネット株式会社",
 "営業部", 23, "朝霞市", "朝志ヶ丘", "朝志ヶ丘ビルディング", 3, "OliveNet", "user2@gmail.com" );
INSERT INTO USER_TABLE (user_id, lastname, firstname, lastyomi, firstyomi,
tel1, tel2, tel3, zip1, zip2, company, department, prefecture, city, town, building,
status, password, mail_adr) VALUES
(13, "鈴木", "三郎", "すずき", "さぶろう", "090", "1234", "5678", "100", "0035", "オリーブネット株式会社",
 "営業部", 23, "朝霞市", "朝志ヶ丘", "朝志ヶ丘ビルディング", 3, "OliveNet", "user3@gmail.com" );
INSERT INTO USER_TABLE (user_id, lastname, firstname, lastyomi, firstyomi,
tel1, tel2, tel3, zip1, zip2, company, department, prefecture, city, town, building,
status, password, mail_adr) VALUES
(14, "鈴木", "史郎", "すずき", "しろう", "090", "1234", "5678", "100", "0035", "オリーブネット株式会社",
 "営業部", 23, "朝霞市", "朝志ヶ丘", "朝志ヶ丘ビルディング", 3, "OliveNet", "user4@gmail.com" );
INSERT INTO USER_TABLE (user_id, lastname, firstname, lastyomi, firstyomi,
tel1, tel2, tel3, zip1, zip2, company, department, prefecture, city, town, building,
status, password, mail_adr) VALUES
(15, "鈴木", "吾郎", "すずき", "ごろう", "090", "1234", "5678", "100", "0035", "オリーブネット株式会社",
 "営業部", 23, "朝霞市", "朝志ヶ丘", "朝志ヶ丘ビルディング", 3, "OliveNet", "user5@gmail.com" );
INSERT INTO USER_TABLE (user_id, lastname, firstname, lastyomi, firstyomi,
tel1, tel2, tel3, zip1, zip2, company, department, prefecture, city, town, building,
status, password, mail_adr) VALUES
(16, "鈴木", "六郎", "すずき", "ろくろう", "090", "1234", "5678", "100", "0035", "オリーブネット株式会社",
 "営業部", 23, "朝霞市", "朝志ヶ丘", "朝志ヶ丘ビルディング", 3, "OliveNet", "user6@gmail.com" );
INSERT INTO USER_TABLE (user_id, lastname, firstname, lastyomi, firstyomi,
tel1, tel2, tel3, zip1, zip2, company, department, prefecture, city, town, building,
status, password, mail_adr) VALUES
(17, "鈴木", "七郎", "すずき", "しちろう", "090", "1234", "5678", "100", "0035", "オリーブネット株式会社",
 "営業部", 23, "朝霞市", "朝志ヶ丘", "朝志ヶ丘ビルディング", 3, "OliveNet", "user7@gmail.com" );
INSERT INTO USER_TABLE (user_id, lastname, firstname, lastyomi, firstyomi,
tel1, tel2, tel3, zip1, zip2, company, department, prefecture, city, town, building,
status, password, mail_adr) VALUES
(18, "鈴木", "八郎", "すずき", "はちろう", "090", "1234", "5678", "100", "0035", "オリーブネット株式会社",
 "営業部", 23, "朝霞市", "朝志ヶ丘", "朝志ヶ丘ビルディング", 3, "OliveNet", "user8@gmail.com" );
INSERT INTO USER_TABLE (user_id, lastname, firstname, lastyomi, firstyomi,
tel1, tel2, tel3, zip1, zip2, company, department, prefecture, city, town, building,
status, password, mail_adr) VALUES
(19, "鈴木", "九郎", "すずき", "クロウ", "090", "1234", "5678", "100", "0035", "オリーブネット株式会社",
 "営業部", 23, "朝霞市", "朝志ヶ丘", "朝志ヶ丘ビルディング", 3, "OliveNet", "user9@gmail.com" );
INSERT INTO USER_TABLE (user_id, lastname, firstname, lastyomi, firstyomi,
tel1, tel2, tel3, zip1, zip2, company, department, prefecture, city, town, building,
status, password, mail_adr) VALUES
(20, "鈴木", "十郎", "すずき", "じゅうろう", "090", "1234", "5678", "100", "0035", "オリーブネット株式会社",
 "営業部", 23, "朝霞市", "朝志ヶ丘", "朝志ヶ丘ビルディング", 3, "OliveNet", "user10@gmail.com" );

UPDATE USER_TABLE SET PASSWORD = '+LoobSdUAt7Uc2bABJgF9gtl2CVZDRX8jJVT4jcCxr7VFh8auBTppFC0zQUWtRI4' where user_id=11;

