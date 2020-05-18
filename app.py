from flask import Flask, request 
from flask import Response
import pandas as pd
import sqlite3
app = Flask(__name__) 

# Menampilkan tabel albums (static 1)
@app.route('/albums')
def albums():
    conn = sqlite3.connect("data/chinook.db")
    albums = pd.read_sql_query("SELECT * FROM albums", conn) 
    return(albums.to_json())

# Menampilkan tabel employees (static 2)
@app.route('/employees')
def employees():
    conn = sqlite3.connect("data/chinook.db")
    albums = pd.read_sql_query("SELECT * FROM employees", conn)
    return(albums.to_json())

# Menampilkan Dataframe Invoice (static 3)
@app.route('/invoice', methods=['GET'])
def get_inv():
    conn = sqlite3.connect('data/chinook.db')
    inv = pd.read_sql_query('''
    SELECT InvoiceLineId, t.Name as Song, alb.Title as AlbumName, art.Name as ArtistName, Quantity
    FROM invoice_items as invt
    LEFT JOIN tracks as t
    ON t.TrackId = invt.TrackId
    LEFT JOIN albums as alb
    ON alb.AlbumId = t.AlbumId
    LEFT JOIN artists as art
    ON art.ArtistId = alb.ArtistId
    ''', conn)
    inv.stack(level=0).unstack(level=1)
    return(inv.to_json())

# Nama lengkap employee yang melayani customer paling banyak (dinamyc 1)
@app.route('/customer/name/<employees>', methods=['GET'])
def get_name(employees):
    conn = sqlite3.connect('data/chinook.db')
    name = pd.read_sql_query ('''
                              SELECT employees.firstname,
                              employees.lastname,
                              count(customers.supportrepid) as total
                              FROM customers
                              LEFT JOIN employees ON customers.supportrepid = employees.employeeid
                              GROUP BY customers.supportrepid
                              ORDER BY total DESC
                              ''', conn)
    return (name.to_json())

# Lima penjualan terbaik berdasarkan GenreID (dinamyc 2)
@app.route('/top/genre/<genreid>', methods=['GET'])
def get_genre(genreid):
    conn = sqlite3.connect('data/chinook.db')
    top_genre = pd.read_sql_query("SELECT genres.GenreId, genres.Name,SUM(invoices.Total) as Total, SUM(Invoice_Items.quantity) as quantity \
                               FROM tracks \
                               LEFT JOIN genres ON genres.GenreId=tracks.GenreId \
                               LEFT JOIN invoice_items on invoice_items.trackid=tracks.trackid \
                               LEFT JOIN invoices on invoices.invoiceid=invoice_items.invoiceid \
                               GROUP BY genres.GenreId \
                               ORDER BY Total DESC \
                               LIMIT 5", 
                               conn)
    return (top_genre.to_json())

@app.route('/')
def welcome():
    return '''<h1> Selamat Datang di Project Agus Setyawan</h1>'''

@app.route("/docs")
def documentation():
    return '''
        <h1> Documentation </h1>
        <h2> Static Endpoints 1 </h2>
        <ol>
            <li>
                <p> '/albums', method = GET </p>
                <p> Menampilkan tabel albums </p>
            </li>
        </ol>
         
        <h2> Static Endpoints 2 </h2>
        <ol>
            <li>
                <p> '/employees', method = GET </p>
                <p> Menampilkan tabel employees </p>
            </li>
        </ol>

        <h2> Static Endpoints 3 </h2>
        <ol>
            <li>
                <p> '/invoice', method = GET </p>
                <p> Menampilkan Dataframe Invoice </p>
            </li>
        </ol>

        <h2> Dynamic Endpoints 1 </h2>
        <ol>
            <li>
                <p> '/customer/name/<employees>' , method = GET </p>
                <p> Nama lengkap employee yang melayani customer paling banyak </p>
				<li> Chinook.db </li>
                   
            </li>
 
        	</ol>

        <h2> Dynamic Endpoints 2 </h2>
        <ol>
            <li>
                <p> '/top/genre/<genreid>' , method = GET </p>
                <p> Lima penjualan terbaik berdasarkan GenreID </p>
				<li> Chinook.db </li>
                   
            </li>
 
        	</ol>
    '''

if __name__ == '__main__':
    app.run(debug=True, port=5000)
