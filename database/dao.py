from database.DB_connect import DBConnect

class DAO:
    @staticmethod
    def get_years():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT DISTINCT YEAR(s_datetime) as year
                    FROM sighting
                    ORDER BY year"""

        cursor.execute(query)

        for row in cursor:
            result.append(row["year"])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_shape(year):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT DISTINCT shape
                    FROM sighting
                    WHERE YEAR(s_datetime) = %s"""

        cursor.execute(query, (year,))

        for row in cursor:
            result.append(row["shape"])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_state():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT DISTINCT id
                    FROM state"""

        cursor.execute(query)

        for row in cursor:
            result.append(row["id"])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_connection():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT state1, state2
                    FROM neighbor"""

        cursor.execute(query)

        for row in cursor:
            result.append((row["state1"], row["state2"]))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_avvistamenti(year, shape):
        conn = DBConnect.get_connection()

        result = {}

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT s.id, COUNT(DISTINCT i.id) as count
                    FROM state s, sighting i
                    WHERE s.id = i.state
                    AND YEAR(i.s_datetime) = %s
                    AND i.shape = %s
                    GROUP BY s.name"""

        # E' OBBLIGATORIO FARE IL GROUP BY QUANDO SI USA IL COUNT!!

        cursor.execute(query, (year, shape))

        for row in cursor:
            result[row["id"]] = row["count"]

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_lat_long():
        conn = DBConnect.get_connection()

        result = {}

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT state, latitude, longitude
                    FROM sighting"""

        # E' OBBLIGATORIO FARE IL GROUP BY QUANDO SI USA IL COUNT!!

        cursor.execute(query)

        for row in cursor:
            result[row["state"].upper()] = (row["latitude"], row["longitude"])

        cursor.close()
        conn.close()
        return result