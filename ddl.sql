CREATE TYPE mem_type AS ENUM ('picture', 'video', 'gif', 'coub', 'pasta');

CREATE TABLE mems
(
	mem_id integer PRIMARY KEY,
	--pics
	name varchar(30) NOT NULL UNIQUE,
	type() mem_type,
	origin text DEFAULT "Who knows ¯\_(ツ)_/¯"
);
