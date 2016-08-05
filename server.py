# Download images from Google Drive by PyDrive from https://github.com/googledrive/PyDrive
import logging
import json
import tornado.httpserver
import tornado.ioloop
import tornado.web
import os
import io
import extractobject
import datetime 
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from tornado.escape import json_encode

OUT_PATH = "{base_path}/out/".format(base_path=os.path.abspath(os.path.dirname(__file__)))
DOWNLOAD_PATH = "{base_path}/images".format(base_path=os.path.abspath(os.path.dirname(__file__)))

def download(file_id, path=DOWNLOAD_PATH):
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)

    file_list = drive.ListFile({'q':"'%s' in parents and trashed=false" % file_id}).GetList()
    for file1 in file_list:
        if file1['title'].lower().endswith(('.jpg','.jpeg','.png')):
            imgf = drive.CreateFile({'id':file1['id']})
            imgf.GetContentFile(DOWNLOAD_PATH + '/'+ file1['title'])
 
class MyHandler(tornado.web.RequestHandler):
    def post(self):
        if self.request.body:
           try:
                # Get parameters when client send curl 
                data = json.loads(self.request.body.decode('utf-8'))
                logging.info('Got JSON data from curl') 
                self.num_thread = data.get("number_thread", None)
                self.inpath = data.get("path", None)
                logging.info('Download from Google drive')

                parsepath = self.inpath.split("/")
                folder_id =  parsepath[-1]
                
                #Download from Google Drive and save in local "/images"
                #download(folder_id)
                
                start = datetime.datetime.now() 
                print(start)
                totalnum = extractobject.multithreadtask(self.num_thread)
                stop = datetime.datetime.now()
  
                total_processing_time = stop - start
                total_processing_time = int((total_processing_time.total_seconds() * 1000))
                avg_processing_time = float("{0:.2f}".format(total_processing_time/totalnum))
                
                response_obj = {"average_processing_time_ms": avg_processing_time, 
                                "output_dir":OUT_PATH, 
                                "total_processed":totalnum, 
                                "total_processing_time_ms":total_processing_time} 
                self.write(json_encode(response_obj))
           except ValueError:
                self.write({'Unable to parse JSON':400})

if __name__ == '__main__':
    # server listen at port 8888 to get instructions
    app = tornado.web.Application([ tornado.web.url(r'/cut', MyHandler) ])
    logging.basicConfig(filename='myapp.log', level=logging.INFO) 
    logging.info('Starting server on port 8888') 
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(8888)
    tornado.ioloop.IOLoop.instance().start()

