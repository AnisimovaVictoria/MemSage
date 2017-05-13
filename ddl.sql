CREATE TYPE mem_type AS ENUM ('pepe', 'cats', 'dogs');

CREATE SEQUENCE auto_id_mems;
CREATE TABLE public.memes
(
  mem_id integer NOT NULL DEFAULT nextval('auto_id_mems'::regclass),
  file_id text NOT NULL default '0'::text,
  name character varying(30) NOT NULL,
  type mem_type DEFAULT 'pepe'::mem_type,
  gustas integer DEFAULT 0,
  origin text DEFAULT 'Who knows ¯\_(ツ)_/¯'::text,
  CONSTRAINT memes_pkey PRIMARY KEY (mem_id),
  CONSTRAINT unique_name UNIQUE (name)
)

CREATE TYPE floor AS ENUM ('linoleum', 'laminate', 'kovrolin', 'keramogranit', 'parquet', 'hardwood', 'self-leveling');
CREATE TYPE sp_type AS ENUM ('FOREVER ALONE((', 'IN LOVE', 'ЕСТЬ ЕДА', 'ВСЕ ОЧЕНЬ СЛОЖНА');
CREATE TYPE occup_type AS ENUM ('pre!shkolyar', 'shkolyar', 'fiztech!shkolyar', 'post!shkolyar');

CREATE SEQUENCE auto_id_bros;

CREATE TABLE public.bros
(
  bro_id integer NOT NULL DEFAULT nextval('auto_id_bros'::regclass),
  name character varying(20) NOT NULL,
  gender floor DEFAULT 'linoleum'::floor,
  sp sp_type DEFAULT 'forever alone'::sp_type,
  occupation occup_type DEFAULT 'shkolyar'::occup_type,
  city character varying(30),
  is_hikka boolean DEFAULT true,
  fav_mem mem_type DEFAULT 'pepe'::mem_type,
  CONSTRAINT bros_pkey PRIMARY KEY (bro_id)
)
-- DROP INDEX public.bro_id_idx;

CREATE UNIQUE INDEX bro_id_idx
  ON public.bros
  USING btree
  (bro_id);


CREATE TYPE status_type AS ENUM ('follower', 'rejected', 'in black list');
--первый подписан на второго, первый отказал в дружбе второму, первый добавил второго в черный литс
CREATE TABLE relationships
(
	first_bro integer REFERENCES bros(bro_id),
	second_bro integer REFERENCES bros(bro_id),
	status status_type,
	PRIMARY KEY (first_bro, second_bro)
);



CREATE TABLE public.megustas
(
  mem_id integer NOT NULL,
  bro_id integer NOT NULL,
  data date DEFAULT current_date,
  CONSTRAINT megustas_pkey PRIMARY KEY (mem_id, bro_id)
);

