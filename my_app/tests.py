import my_app
import unittest
import os
import sqlalchemy
import psycopg2
import testing.postgresql
from time import sleep
import shutil
import pg8000

ITS_CAT = 'Это кот, а не хлеб! Не ешь его!'

class TestPostgresql(unittest.TestCase):
    def test_basic(self):
        try:
            pgsql = testing.postgresql.Postgresql()
            self.assertIsNotNone(pgsql)
            params = pgsql.dsn()
            self.assertEqual('test', params['database'])
            self.assertEqual('127.0.0.1', params['host'])
            self.assertEqual(pgsql.settings['port'], params['port'])
            self.assertEqual('postgres', params['user'])

            conn = psycopg2.connect(**pgsql.dsn())
            self.assertIsNotNone(conn)
            conn.close()

            engine = sqlalchemy.create_engine(pgsql.url())
            self.assertIsNotNone(engine)

        finally:
            pid = pgsql.server_pid
            self.assertTrue(pgsql.is_alive())

            pgsql.stop()
            sleep(1)

            self.assertFalse(pgsql.is_alive())
            with self.assertRaises(OSError):
                os.kill(pid, 0)

    def test_dsn_and_url(self):
        pgsql = testing.postgresql.Postgresql(port=12345, auto_start=0)
        self.assertEqual({'database': 'test', 'host': '127.0.0.1', 'port': 12345, 'user': 'postgres'},
                         pgsql.dsn())
        self.assertEqual("postgresql://postgres@127.0.0.1:12345/test", pgsql.url())

class TestBot(unittest.TestCase):
    def setUp(self):
        print('### Setting up flask server ###')
        my_app.app.testing = True
        self.app = my_app.app.test_client()

    def test_get_history(self):
        history_000 = """<style>#input_message{
                    display: inline_block;
                    position: fixed; 
                    margin-top: 10px;
                    bottom: 0;
                    }
                    .name_bot{
                    font: bold 2em Arial, Tahome, sans-serif;
                    position: fixed;
                    width: 100%;
                    margin-bottom: 10px; 
                    text-align: center;
                    top: 0;
                    }
                    scroll-container {
                    outline: 2px solid #000;
                    display: block;
                    height: 90%;
                    margin: 50px auto 20px;
                    overflow-y: auto;
                    }
</style>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js"></script>
<body>
<div class="name_bot">EORA - your personal bot</div>
<scroll-container>
Привет, 000!!! Я помогу отличить кота от хлеба! Объект перед тобой квадратный?<br />2019-08-27 02:49<br />"""
        if my_app.get_history("000") == history_000:
            print("Test get_history(000) is OK")
        else:
            print("Test get_history(000) is Fail")

    def test_get_last_status(self):
        last_status_000 = 0
        if my_app.get_last_status("000") == last_status_000:
            print("Test get_last_status(000) is OK")
        else:
            print("Test get_last_status(000) is Fail")

    def test_prediction_and_test_post(self):
        shutil.copy(r'Leicester_City.png',r'src/Leicester_City.png')
        if my_app.prediction("Leicester_City.png","909") == ITS_CAT:
            print("Test prediction(Leicester_City.png,999) is OK")
        else:
            print("Test prediction(Leicester_City.png,999) is Fail")

    def test_get_bot_response(self):
        resp = self.app.get('/eora/api/')
        self.assertEqual(resp.status_code, 200)
        resp = self.app.get('/eora/api/?user_id=999')
        self.assertEqual(resp.status_code, 200)
        resp = self.app.get('/eora/api/?msg=да&user_id=909')
        self.assertEqual(resp.status_code, 200)

if __name__ == '__main__':
    unittest.main()