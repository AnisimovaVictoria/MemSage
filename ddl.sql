CREATE TYPE mem_type AS ENUM ('picture', 'video', 'gif', 'coub', 'pasta', 'text');
CREATE TABLE memes
(
	mem_id integer PRIMARY KEY,
	picture_filename varchar(50) NOT NULL,
	name varchar(30) NOT NULL,
	type mem_type,
	origin text DEFAULT 'Who knows ¯\_(ツ)_/¯',
	CONSTRAINT unique_picture UNIQUE(picture_filename),
	CONSTRAINT unique_name UNIQUE(name)
);

CREATE TYPE floor AS ENUM ('linoleum', 'laminate', 'kovrolin', 'keramogranit', 'parquet', 'hardwood', 'self-leveling');
CREATE TYPE sp_type AS ENUM ('forever alone', 'IN LOVE');
CREATE TABLE public.bros
(
  bro_id integer PRIMARY KEY,
  name character varying(20) NOT NULL, -- Имя пользователя
  password character varying(30), -- Пароль
  fav_mem integer REFERENCES memes(mem_id), -- Любимый мем
  SP sp_type, -- семейное положение
  occupation character varying(30), -- деятельность
  city character varying(30), -- город
  gender floor, --гендер пользователя
  CHECK (length(password) >= 9)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.bros
  OWNER TO postgres;
  
CREATE TABLE memsages
 (
 	memsage_id integer PRIMARY KEY,
 	sender integer REFERENCES bros(bro_id) NOT NULL,
 	reciever integer REFERENCES bros(bro_id) NOT NULL,
 	send_time date NOT NULL,
 	attached_mem integer REFERENCES memes(mem_id) NOT NULL,
 	comment text
 );
 
CREATE TYPE status_type AS ENUM ('follower', 'rejected', 'in black list')
--первый подписан на второго, первый отказал в дружбе второму, первый добавил второго в черный литс
CREATE TABLE relationships
(
	first_bro integer REFERENCES bros(bro_id),
	second_bro integer REFERENCES bros(bro_id),
	status status_type,
	PRIMARY KEY (first_bro, second_bro)
);

CREATE TABLE megustas
(
	mem_id integer REFERENCES memes(mem_id),
	bro_id integer REFERENCES bros(bro_id),
	PRIMARY KEY (mem_id, bro_id)
);

CREATE TABLE posts
 (
	post_id integer PRIMARY KEY,
 	sender integer REFERENCES bros(bro_id) NOT NULL,
 	postime date NOT NULL,
 	attached_mem integer REFERENCES memes(mem_id) NOT NULL,
 	comment text
 );
