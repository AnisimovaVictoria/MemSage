-- DROP FUNCTION public.set_like() CASCADE;

CREATE OR REPLACE FUNCTION public.set_like()
  RETURNS trigger AS
$BODY$
BEGIN 

UPDATE memes
SET gustas = gustas + 1
WHERE memes.mem_id = NEW.mem_id;
return OLD;

END; 
$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION public.set_like()
  OWNER TO postgres;

CREATE TRIGGER set_gust
AFTER INSERT ON megustas FOR EACH ROW 
EXECUTE PROCEDURE set_like();



-- DROP FUNCTION public.remove_like() CASCADE;

CREATE OR REPLACE FUNCTION public.remove_like()
  RETURNS trigger AS
$BODY$
BEGIN 

UPDATE memes
SET gustas = gustas - 1
WHERE memes.mem_id = OLD.mem_id;
return NEW;

END; 
$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION public.set_like()
  OWNER TO postgres;

CREATE TRIGGER remove_gust
AFTER DELETE ON megustas FOR EACH ROW 
EXECUTE PROCEDURE remove_like();





-- DROP FUNCTION public.remove_user_likes() CASCADE;

CREATE OR REPLACE FUNCTION public.remove_user_likes()
  RETURNS trigger AS
$BODY$
BEGIN 

DELETE ON megustas
WHERE megustas.bro_id = OLD.bro_id;
return NEW;

END; 
$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION public.set_like()
  OWNER TO postgres;

CREATE TRIGGER remove_user
AFTER DELETE ON bros FOR EACH ROW 
EXECUTE PROCEDURE remove_user_likes();
