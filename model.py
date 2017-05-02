import os, os.path
import random
import string
import MySQLdb
from cStringIO import StringIO

import cherrypy
cherrypy.server.socket_host = '0.0.0.0'
cherrypy.config.update({'server.socket_port': 13004})

def connect(thread_index): 
    # Create a connection and store it in the current thread 
    cherrypy.thread_data.db = MySQLdb.connect('localhost', 'root', '', 'blog') 
 
cherrypy.engine.subscribe('start_thread', connect)
 
class Root:
    base_url = "http://localhost:13004"
    @cherrypy.expose
    def index(self): 
        # Sample page that displays the number of records in "table" 
        # Open a cursor, using the DB connection for the current thread 
        c = cherrypy.thread_data.db.cursor() 
        c.execute('select * from tbl_news where visible = 0') 
        res = c.fetchall()
        data = "<a href = '"+str(cherrypy.url())+"AddBerita'><button>Add</button></a>"
        data += "<table border='1'><tr><td>No</td><td>Judul</td><td>Berita</td><td>Tanggal</td><td>Tindakan</td></tr>"
        for row in res:
            judul = row[1]
            berita = row[2]
            data += "<tr><td>%d</td><td>%s</td><td>%s</td><td>%s</td><td><a href='%sAddBerita/%d'><button>Edit</button></a><a href='%sdeleteBerita/%d'><button>Delete</button></a></td></tr>" % (row[0],row[1],row[2],row[3],cherrypy.url(),row[0],cherrypy.url(),row[0])			
        data += "</table>"
        if res:
           return "<html><body>%s</body></html>" % (data) 
        c.close() 
    index.exposed = True 
	
    @cherrypy.expose
    def AddBerita(self, id=None):
        if id<>None:
           c = cherrypy.thread_data.db.cursor() 
           c.execute('select * from tbl_news where visible = 0 and id = '+str(id)) 
           row = c.fetchone()
           return "<html><body><form method='post' action = '/updateBerita/"+str(row[0])+"'><input type='text' name='judul' placeholder = 'Judul' value='"+str(row[1])+"'><br><br><textarea name='berita' placeholder='berita'>"+str(row[2])+"</textarea><br><br><input type='submit' value='simpan'><a href='"+str(cherrypy.url())+"/../'><button>Cancel</button></a></form></body></html>"  
        return "<html><body><form method='post' action = '/InsertBerita/'><input type='text' name='judul' placeholder = 'Judul'><br><br><textarea name='berita' placeholder='berita'></textarea><br><br><input type='submit' value='simpan'><a href='"+str(cherrypy.url())+"/../'><button>Cancel</button></a></form></body></html>"
    AddBerita.exposed = True 
		   
    @cherrypy.expose
    def InsertBerita(self,judul = None,berita = None):
        c = cherrypy.thread_data.db.cursor() 
        c.execute("insert into tbl_news(`judul`,`berita`) values ('"+str(judul)+"','"+str(berita)+"')")
        cherrypy.thread_data.db.commit()
        raise cherrypy.HTTPRedirect('/') 
    InsertBerita.exposed = True

    @cherrypy.expose
    def updateBerita(self,id,judul = None,berita = None):
        c = cherrypy.thread_data.db.cursor() 
        c.execute("update tbl_news set `judul` = '"+str(judul)+"',`berita` = '"+str(berita)+"' where id="+str(id))
        cherrypy.thread_data.db.commit()
        raise cherrypy.HTTPRedirect('/') 
    updateBerita.exposed = True

    @cherrypy.expose
    def deleteBerita(self,id=None):
        c = cherrypy.thread_data.db.cursor() 
        c.execute("delete from tbl_news where id = "+str(id))
        cherrypy.thread_data.db.commit()
        raise cherrypy.HTTPRedirect('/') 
    deleteBerita.exposed = True

if __name__ == '__main__':
    conf = {
	'/': {
		'tools.sessions.on': True,
		'tools.staticdir.root': os.path.abspath(os.getcwd())
	},
	'/static': {
             'tools.staticdir.on': True,
             'tools.staticdir.dir': './public_html'
         }
    }
    cherrypy.quickstart(Root(), "/", conf)