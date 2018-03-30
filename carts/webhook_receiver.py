import hmac
import hashlib
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
import urlparse

PORT = 8000
FILENAME = 'webhook_data.txt'


class MojoHandler(BaseHTTPRequestHandler):
  def do_POST(self):
      content_length = int(self.headers['content-length'])
      querystring = self.rfile.read(content_length)
      data = urlparse.parse_qs(querystring)
      mac_provided = data.pop('mac')
      message = "|".join(v for k, v in sorted(data.items(), key=lambda x: x[0].lower()))
      # Pass the 'salt' without the <>.
      mac_calculated = hmac.new("dfa2eabea337429fb3aebc4b8d7844fb", message, hashlib.sha1).hexdigest()
      if mac_provided == mac_calculated:
          if data['status'] == "Credit":
              pass
              # Payment was successful, mark it as completed in your database.
          else:
              pass
              # Payment was unsuccessful, mark it as failed in your database.
          self.send_response(200)
      else:
          self.send_response(400)
      self.send_header('Content-type', 'text/html')
      self.end_headers()

httpd = HTTPServer(('', PORT), MojoHandler)
httpd.serve_forever()
