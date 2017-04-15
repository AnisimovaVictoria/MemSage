CREATE TYPE mem_type AS ENUM ('picture', 'video', 'gif', 'coub', 'pasta');
CREATE TABLE mems
(
	mem_id integer PRIMARY KEY,
	--pics
	name varchar(30) NOT NULL,
	type mem_type,
	origin text DEFAULT 'Who knows ¯\_(ツ)_/¯',
	CONSTRAINT unique_name UNIQUE(name)
);

CREATE TYPE floor AS ENUM ('linoleum', 'laminat', 'kovrolin', 'keramogranit', 'parket');
CREATE TABLE public.bros
(
  bro_id integer PRIMARY KEY,
  name character varying(20) NOT NULL, -- Имя пользователя
  SP character varying(30), -- семейное положение
  gender floor,
  UNIQUE(bro_id)
)

CREATE TABLE memsages
(
	memsage_id integer PRIMARY KEY,
	sender integer REFERENCES bros(bro_id) NOT NULL,
	reciever integer REFERENCES bros(bro_id) NOT NULL,
	send_time date NOT NULL,
	attached_mem integer REFERENCES memes(mem_id) NOT NULL,
	comment text
)
