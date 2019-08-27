# EORA - your personal bot

# _Test ChatBot EORA_

## Description:
Test ChatBot on *Python 3.5* on localhost, which can predict cat and bread. 

## Installation:
1. Download:
  * Clone repository:
    [clone githab](https://github.com/Lehsuby/chatbotEORA.git)

     or
     
  * Install package and download additional files for tensorflow from [Google Drive](https://drive.google.com/open?id=1HA0MunsTQbvg4x-hGlwy2zxE29xq2Spv)
```python
    pip install chatboteora
```
2. Create DB in Postgresql:
  * change options
    ```python
    con = psycopg2.connect(dbname='db_chatbotEORA', user='tu', host='localhost', password='qwerty')
    ```
  * create scrypts
    ```SQL
    -- create db
    CREATE DATABASE "db_chatbotEORA"
    WITH OWNER = tu
       ENCODING = 'UTF8'
       TABLESPACE = pg_default
       LC_COLLATE = 'ru_RU.UTF-8'
       LC_CTYPE = 'ru_RU.UTF-8'
       CONNECTION LIMIT = -1;
       
    -- create users table
    CREATE TABLE public.users
    (
      user_id text NOT NULL,
      CONSTRAINT user_pk PRIMARY KEY (user_id)
    )
    WITH (
      OIDS=FALSE
    );
    ALTER TABLE public.users
      OWNER TO tu;
    
    -- create answers table
    CREATE TABLE public.answers
    (
      message text,
      time_message timestamp without time zone NOT NULL,
      user_id text,
      task_status smallint NOT NULL DEFAULT 0,
      sender boolean NOT NULL,
      CONSTRAINT user_id_fk FOREIGN KEY (user_id)
          REFERENCES public.users (user_id) MATCH SIMPLE
          ON UPDATE NO ACTION ON DELETE NO ACTION
    )
    WITH (
      OIDS=FALSE
    );
    ALTER TABLE public.answers
      OWNER TO tu;
    ```
    
## QUICK START
### * First run:
![Hello page](https://github.com/Lehsuby/chatbotEORA/blob/master/1.png?raw=true)
### * Insert your nickname and then give main page:
![Main page](https://github.com/Lehsuby/chatbotEORA/blob/master/2.png?raw=true)
### * Some examples:
![Main page](https://github.com/Lehsuby/chatbotEORA/blob/master/3.png?raw=true)
![Main page](https://github.com/Lehsuby/chatbotEORA/blob/master/4.png?raw=true)
![Main page](https://github.com/Lehsuby/chatbotEORA/blob/master/5.png?raw=true)

# Conclusion
Thanks TensorFlow for their scrypts.

__Not for commercial use__
