import logging, sys, os, tornado.ioloop, tornado.web, tornado.gen, tornado.concurrent

# settings
PORT        = 8888
DEBUG       = True

# global values

g_a_messages = []
g_a_waiters = set()
g_b_messages = []
g_b_waiters = set()

g_a_list = []
g_b_list = []

g_correct = 0
g_correct_waiters = set()
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')
        
class A_NewHandler(tornado.web.RequestHandler):
    def post(self):
        a_message = self.get_argument("message")
        g_a_messages.append(a_message)
        
        for future in g_a_waiters:
            
            future.set_result(g_a_messages)
        self.append_to_list(a_message)
        g_a_waiters.clear()
        
    def append_to_list(self,message):
        g_a_list.append(message)

class A_UpdateHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def post(self):
        # Browser sends the number of messages it has seen so far
        num_seen = int(self.get_argument("num_seen",0))
        
        if num_seen == len(g_a_messages):
            
            self._future = tornado.concurrent.Future()
            g_a_waiters.add(self._future)
            yield self._future
        
        if not self.request.connection.stream.closed():
            self.write({"messages":g_a_messages})
    def on_connection_close(self):
        g_a_waiters.remove(self._future)
        self._future.set_result([])

class B_NewHandler(tornado.web.RequestHandler):
    def post(self):
        b_message = self.get_argument("message")
        g_b_messages.append(b_message)
        
        for future in g_b_waiters:
            
            future.set_result(g_b_messages)
        
        self.append_to_list(b_message)
        g_b_waiters.clear()
    
    def append_to_list(self,message):
        g_b_list.append(message)

class B_UpdateHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def post(self):
        # Browser sends the number of messages it has seen so far
        num_seen = int(self.get_argument("num_seen",0))
        
        if num_seen == len(g_b_messages):
            
            self._future = tornado.concurrent.Future()
            g_a_waiters.add(self._future)
            yield self._future
        
        if not self.request.connection.stream.closed():
            self.write({"messages":g_b_messages})
    def on_connection_close(self):
        g_b_waiters.remove(self._future)
        self._future.set_result([])

class CompareHandler(tornado.web.RequestHandler):
    def post(self):
        # make sure g_a_list and g_b_list is not null, use length
        # declare arguments
        length_a = len(g_a_list)
        length_b = len(g_b_list)
        if self.check_a_b(g_a_list,g_b_list):
            if g_a_list(length_a-1) == g_b_list(length_b-1):
                # send something back to browser and clear the list
                g_correct = g_correct + 1
                del g_a_list[:]
                del g_b_list[:]
                
            else:
                # list keep on and nothing happen
                print"nothing"
        for future in g_correct_waiters:
            
            future.set_result(g_correct)
        
        g_correct_waiters.clear()
        
    def check_a_b(self,a_list,b_list):
        length_a = len(a_list)
        length_b = len(b_list)
        if length_a != 0 and length_b != 0:
            return True
        else:
            return False

class UpdateCompareHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def post(self):
        correct = self.get_argument("correct",0)
        if correct == g_correct:
            self._future = tornado.concurrent.Future()
            g_correct_waiters.add(self._future)
            yield self._future
        
        if not self.request.connection.stream.closed():
            self.write({"correct":g_correct})

    def on_connection_close(self):
        g_correct_waiters.remove(self._future)
        self._future.set_result([])
        
if __name__ == "__main__":
    def main():
        app = tornado.web.Application(
            [ (r"/",       MainHandler),
              (r"/new_a",    A_NewHandler),
              (r"/update_a", A_UpdateHandler),
              (r"/new_b",    B_NewHandler),
              (r"/update_b", B_UpdateHandler),
              (r"/compare", CompareHandler),
              (r"/update_compate",    UpdateCompareHandler)
               ],
            template_path = os.path.join(os.path.dirname(__file__), "templates"),
            static_path   = os.path.join(os.path.dirname(__file__), "static"),
            debug         = DEBUG,
        )

        # Start the HTTP server and the IOLoop.  (These work together.)
        app.listen(port=PORT)
        sys.stderr.write("Starting server at http://localhost:%d\n"%PORT)
        tornado.ioloop.IOLoop.instance().start()

    main()
