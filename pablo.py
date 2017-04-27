# coding=utf-8
import MySQLdb
dbName = "pablo"
user = "root"
passwd = ""
host = "localhost"
port = 3306


class Pablo:


    def __init__(self):
        "Etablissement connexion et creation curseur"
        try:
            self.bdd = MySQLdb.connect(db=dbName, user=user, passwd=passwd, host=host, port=port)
        except Exception as e:
            self.fail_connect = 1
            print("Connexion Error : %s", e)
        else:
            self.fail_connect = 0
            self.cursor = self.bdd.cursor()
        self.bdd.set_character_set('utf8')
        self.cursor.execute('SET NAMES utf8;')
        self.cursor.execute('SET CHARACTER SET utf8;')
        self.cursor.execute('SET character_set_connection=utf8;')

    def executerReq(self, req):
        "Exécution de la requête <req>, avec détection d'erreur éventuelle"
        try:
            self.cursor.execute(req)
        except Exception, err:
            # afficher la requête et le message d'erreur système :
            print "Requête SQL incorrecte :\n%s\nErreur détectée :\n%s" % (req, repr(err))
            return 0
        else:
            return 1

    def resultatReq(self):
        "renvoie le résultat de la requête précédente (un tuple de tuples)"
        return self.cursor.fetchall()

    def commit(self):
        if self.bdd:
            self.bdd.commit()         # transfert curseur -> disque

    def close(self):
        if self.bdd:
            self.bdd.close()

    def last_insert_id(self):
        self.cursor.execute('SELECT last_insert_id()')
        return int(self.cursor.fetchone()[0])

    def id_product(self, product_name):
        self.executerReq('SELECT id from product where name = "{}"'.format(product_name))
        result = self.cursor.fetchone()
        if result:
            return int(result[0])
        else:
            return None

    def create_product(self, name):
        """create a row in product table with name parameter and return id
            create_product(self, name) => id (int)"""
        if self.id_product(name):
            raise ValueError ("There is already a product with that name")
        else:
            self.executerReq('INSERT INTO product (name) VALUES ("{}")'.format(name))
            return (self.last_insert_id())

    def exec_req_with_args(self, req, args):
        try:
            self.cursor.execute(req, args)
        except Exception, err:
            print "Requête SQL incorrecte :\n%s\nErreur détectée :\n%s" % (req, repr(err))
            return 0
        else:
            return 1


    def get_id_source(self, name):
        self.executerReq('SELECT id from source where name = "{}"'.format(name))
        result = self.cursor.fetchone()
        if result:
            return int(result[0])
        else:
            return None
