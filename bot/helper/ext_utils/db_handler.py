import psycopg2
from psycopg2 import Error
from bot import AUTHORIZED_CHATS, SUDO_USERS, DB_URI, LOGGER

class DbManger:
    def __init__(self):
        self.err = False

    def connect(self):
        try:
            self.conn = psycopg2.connect(DB_URI)
            self.cur = self.conn.cursor()
        except psycopg2.DatabaseError as error :
            LOGGER.error("Error in dbMang : ", error)
            self.err = True

    def disconnect(self):
        self.cur.close()
        self.conn.close()

    def db_auth(self,chat_id: int):
        self.connect()
        if self.err:
            return "Ada beberapa log pemeriksaan kesalahan untuk detailnya"
        sql = 'INSERT INTO users VALUES ({});'.format(chat_id)
        self.cur.execute(sql)
        self.conn.commit()
        self.disconnect()
        AUTHORIZED_CHATS.add(chat_id)
        return 'Diotorisasi dengan sukses'

    def db_unauth(self,chat_id: int):
        self.connect()
        if self.err:
            return "Ada beberapa log pemeriksaan kesalahan untuk detailnya"
        sql = 'DELETE from users where uid = {};'.format(chat_id)
        self.cur.execute(sql)
        self.conn.commit()
        self.disconnect()
        AUTHORIZED_CHATS.remove(chat_id)
        return 'Berhasil tidak diotorisasi'

    def db_addsudo(self,chat_id: int):
        self.connect()
        if self.err:
            return "Ada beberapa log pemeriksaan kesalahan untuk detailnya"
        if chat_id in AUTHORIZED_CHATS:
            sql = 'UPDATE users SET sudo = TRUE where uid = {};'.format(chat_id)
            self.cur.execute(sql)
            self.conn.commit()
            self.disconnect()
            SUDO_USERS.add(chat_id)
            return 'Berhasil dipromosikan sebagai Sudo'
        else:
            sql = 'INSERT INTO users VALUES ({},TRUE);'.format(chat_id)
            self.cur.execute(sql)
            self.conn.commit()
            self.disconnect()
            SUDO_USERS.add(chat_id)
            return 'Berhasil Diotorisasi dan dipromosikan sebagai Sudo'

    def db_rmsudo(self,chat_id: int):
        self.connect()
        if self.err:
            return "Ada beberapa log pemeriksaan kesalahan untuk detailnya"
        sql = 'UPDATE users SET sudo = FALSE where uid = {};'.format(chat_id)
        self.cur.execute(sql)
        self.conn.commit()
        self.disconnect()
        SUDO_USERS.remove(chat_id)
        return 'Berhasil dihapus dari Sudo'
