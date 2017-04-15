CREATE TYPE mem_type AS ENUM ('picture', 'video', 'gif', 'coub', 'pasta');

CREATE TABLE mems
(
	mem_id integer PRIMARY KEY,
	--pics
	name varchar(30) NOT NULL,
	type() mem_type,
	origin text DEFAULT "Who knows ¯\_(ツ)_/¯",
	CONSTRAINT unique_name UNIQUE(name)
);
