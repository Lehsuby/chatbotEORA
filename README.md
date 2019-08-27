# EORA - your personal bot

# Test ChatBot EORA

## Installation:
1.1. Clone githab repository:
[clone githab](https://github.com/Lehsuby/chatbotEORA.git)

1.2. Create DB in Postgresql:
  * change options
  * create scrypts
    '''
    //create db
    CREATE DATABASE "db_chatbotEORA"
  WITH OWNER = tu
       ENCODING = 'UTF8'
       TABLESPACE = pg_default
       LC_COLLATE = 'ru_RU.UTF-8'
       LC_CTYPE = 'ru_RU.UTF-8'
       CONNECTION LIMIT = -1;
       
    //create users table
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
    
    //create answers table
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
    '''
    
Please make sure the release file is unpacked under a Web-accessible directory. You shall see the following files and directories:

  demos/               demos
  framework/           framework source files
  requirements/        requirement checker
  CHANGELOG            describing changes in every Yii release
  LICENSE              license of Yii
  README               this file
  UPGRADE              upgrading instructions
REQUIREMENTS
The minimum requirement by Yii is that your Web server supports PHP 5.1.0 or above. Yii has been tested with Apache HTTP server on Windows and Linux operating systems.

Please access the following URL to check if your Web server reaches the requirements by Yii, assuming "YiiPath" is where Yii is installed:

  http://hostname/YiiPath/requirements/index.php
QUICK START
Yii comes with a command line tool called "yiic" that can create a skeleton Yii application for you to start with.

On command line, type in the following commands:

    $ cd YiiPath/framework                (Linux)
    cd YiiPath\framework                  (Windows)

    $ ./yiic webapp ../testdrive          (Linux)
    yiic webapp ..\testdrive              (Windows)
The new Yii application will be created at "YiiPath/testdrive". You can access it with the following URL:

    http://hostname/YiiPath/testdrive/index.php
WHAT'S NEXT
Please visit the project website for tutorials, class reference and join discussions with other Yii users.

The Yii Developer Team http://www.yiiframework.com
