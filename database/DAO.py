from database.DB_connect import DBConnect
from model.order import Order
from model.store import Store


class DAO():
    @staticmethod
    def getAllStores():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT * from stores"

        cursor.execute(query)

        for row in cursor:
            results.append(Store(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getOrders(storeId):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select *
                from orders o 
                where o.store_id =%s"""
        cursor.execute(query,(storeId,))

        for row in cursor:
            results.append(Order(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getEdges(storeId, k):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT t1.order_id AS id1,t2.order_id AS id2, (t1.quantita_tot + t2.quantita_tot) AS somma_oggetti, 
                    DATEDIFF(t2.order_date, t1.order_date) AS distanza_giorni
                FROM 
                    (SELECT o.order_id, o.order_date, SUM(oi.quantity) AS quantita_tot
                     FROM orders o 
                     JOIN order_items oi ON o.order_id = oi.order_id
                     WHERE o.store_id = %s
                     GROUP BY o.order_id) t1
                JOIN 
                    (SELECT o.order_id, o.order_date, SUM(oi.quantity) AS quantita_tot
                     FROM orders o 
                     JOIN order_items oi ON o.order_id = oi.order_id
                     WHERE o.store_id = %s
                     GROUP BY o.order_id) t2
                ON t1.order_date < t2.order_date
                WHERE DATEDIFF(t2.order_date, t1.order_date) <= %s"""
        cursor.execute(query, (storeId, storeId, k))

        for row in cursor:
            results.append((row["id1"], row["id2"],row["somma_oggetti"],row["distanza_giorni"]))

        cursor.close()
        conn.close()
        return results