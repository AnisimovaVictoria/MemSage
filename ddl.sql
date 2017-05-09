CREATE TYPE mem_type AS ENUM ('picture', 'video', 'gif', 'coub', 'pasta', 'text');

CREATE SEQUENCE auto_id_mems;
CREATE TABLE public.memes
(
  mem_id integer NOT NULL DEFAULT nextval('auto_id_mems'::regclass),
  mem_path character varying(256),
  name character varying(30) NOT NULL,
  type mem_type,
  origin text DEFAULT 'Who knows ¯\_(ツ)_/¯'::text,
  CONSTRAINT memes_pkey PRIMARY KEY (mem_id),
  CONSTRAINT unique_name UNIQUE (name)
);

CREATE TYPE floor AS ENUM ('linoleum', 'laminate', 'kovrolin', 'keramogranit', 'parquet', 'hardwood', 'self-leveling');
CREATE TYPE sp_type AS ENUM ('forever alone', 'IN LOVE');
CREATE TYPE occup_type AS ENUM ('pre!shkolyar', 'shkolyar', 'fiztech!shkolyar', 'post!shkolyar');

CREATE SEQUENCE auto_id_bros;

CREATE TABLE public.bros
(
  bro_id integer NOT NULL DEFAULT nextval('auto_id_bros'::regclass),
  name character varying(20) NOT NULL,
  fav_mem integer DEFAULT 0,
  sp sp_type DEFAULT 'forever alone'::sp_type,
  occupation occup_type DEFAULT 'shkolyar'::occup_type,
  city character varying(30),
  gender floor DEFAULT 'linoleum'::floor,
  CONSTRAINT bros_pkey PRIMARY KEY (bro_id)
);
  
CREATE TABLE memsages
 (
 	memsage_id integer PRIMARY KEY,
 	sender integer REFERENCES bros(bro_id) NOT NULL,
 	reciever integer REFERENCES bros(bro_id) NOT NULL,
 	send_time date NOT NULL,
 	attached_mem integer REFERENCES memes(mem_id) NOT NULL,
 	comment text
 );
 
CREATE TYPE status_type AS ENUM ('follower', 'rejected', 'in black list');
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
