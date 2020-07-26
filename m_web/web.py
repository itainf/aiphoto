import tornado.ioloop
import tornado.web
import m_web.upload as upload
import os


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/eam/fileLocal/upload",    upload.UploadHandler),
        (r"/eam/fileLocal/static",  tornado.web.StaticFileHandler, {"path": "/static"})
    ],
        static_path=os.path.dirname(os.path.dirname(__file__))+"/static"
    )


if __name__ == "__main__":
    current_path = os.path.dirname(__file__)
    app = make_app()
    app.listen(8013)
    tornado.ioloop.IOLoop.current().start()
