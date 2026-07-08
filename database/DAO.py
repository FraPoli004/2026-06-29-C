from database.DB_connect import DBConnect
from model.artista import Artista


class DAO():

    @staticmethod
    def getAllCountries():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """
                select distinct c.Country
                from customer c
                where c.Country is not null
                order by c.Country
                """

        cursor.execute(query)

        for row in cursor:
            results.append(row["Country"])

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllBrani(id):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct t.TrackId as track
                    from album a ,track t 
                    where a.AlbumId =  t.AlbumId  and a.ArtistId = %s"""

        cursor.execute(query,(id,))

        for row in cursor:
            results.append(row["track"])

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllPlaylist(id):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct p.PlaylistId as playlist
                    from album a , track t ,playlisttrack p 
                    where a.AlbumId = t.AlbumId and t.TrackId = p.TrackId
                    and a.ArtistId = %s"""

        cursor.execute(query, (id,))

        for row in cursor:
            results.append(row["playlist"])

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllNodes():  # <-- ADATTA parametri
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct a.ArtistId as ArtistId , a.Name as Name
                    from artist a, album al, track t 
                    where a.ArtistId = al.ArtistId  and al.AlbumId = t.AlbumId
                    and t.TrackId is not null"""
        cursor.execute(query)

        for row in cursor:
            result.append(Artista(row["ArtistId"], row["Name"]))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllEdges():  # <-- ADATTA parametri
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct ct1.ArtistId as nodo1, ct2.ArtistId as nodo2, count(distinct ct1.playlistid ) as peso 
                    from  (select distinct a.ArtistId, p.PlaylistId 
                    from album a, track t , playlisttrack p 
                    where a.AlbumId = t.AlbumId and t.TrackId = p.TrackId ) ct1,
                    (select distinct a.ArtistId, p.PlaylistId 
                    from album a, track t , playlisttrack p 
                    where a.AlbumId = t.AlbumId and t.TrackId = p.TrackId ) ct2
                    where  ct1.playlistid = ct2.playlistid
                    and ct1.artistid < ct2.artistid 
                    group by ct1.ArtistId , ct2.ArtistId"""
        cursor.execute(query)

        for row in cursor:
            result.append((row["nodo1"], row["nodo2"], row["peso"]))
        cursor.close()
        conn.close()
        return result



