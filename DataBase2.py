import sqlite3 as lite
import sys
import pprint


req_task1 = '''
SELECT C.FirstName, C.LastName, C.Phone, C.City FROM Customer C JOIN (
    SELECT C1.City, C1.CustomerId FROM Customer C1
    inner join Invoice 
    on C1.CustomerId = Invoice.CustomerId
    group by C1.City 
    having count(distinct C1.CustomerId) > 1
) TMP1 ON TMP1.City = C.City 
inner join Invoice X on C.CustomerId =X.CustomerId 
group by C.CustomerId;
'''
req_task2 = '''
select c.City, round(sum(i.Total),2) as t from Customer c inner join Invoice I on c.CustomerId = I.CustomerId
group by c.City
order by t DESC
limit 3;
'''
req_task3 = '''
select t.name as GenreName,
       T1.name as Track,
       A.title as Album,
       A2.Name as Artist
FROM (select G.GenreId, G.name
    from InvoiceLine IL
    JOIN Track T ON T.trackId = IL.trackId
    Join Genre G ON G.GenreId = T.GenreId
    group by G.GenreId
    order by sum(quantity) DESC limit 1) t
Join Track T1 ON T1.GenreId  = t.GenreId
LEFT JOIN Album A ON A.AlbumId = T1.AlbumId
LEFT JOIN Artist A2 ON A2.ArtistId = A.artistId
;
'''


def data_out(req_task):
    try:
        connection = lite.connect('Chinook_Sqlite.sqlite')
        cursor = connection.cursor()
        cursor.execute(req_task)

        data = cursor.fetchall()
        pprint.pprint(data)
    except Exception as e:
        print(e)
        sys.exit(1)
    finally:
        if connection is not None:
            connection.close()
    return data
data_out(req_task1)
data_out(req_task2)
data_out(req_task3)