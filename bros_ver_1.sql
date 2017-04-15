
CREATE TYPE floor AS ENUM ('linoleum', 'laminat', 'kovrolin', 'keramogranit', 'parket');
CREATE TABLE public.bros
(
  bro_id integer PRIMARY KEY,
  name character varying(20) NOT NULL, -- Имя пользователя
  SP character varying(30), -- семейное положение
  gender floor,
  UNIQUE(bro_id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.bros
  OWNER TO postgres;

INSERT INTO bros VALUES (0,NULL, 'forever alone', 'laminat');

SELECT *
FROM bros;
