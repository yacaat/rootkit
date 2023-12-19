import http.server
import socketserver
import os
import cgi

class FileUploadHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/upload':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            form_html = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>File Upload Form</title>
            </head>
            <body>
                <h2>File Upload</h2>
                <form action="/" method="post" enctype="multipart/form-data">
                    <label for="file">Select a file:</label>
                    <input type="file" name="file" id="file"><br>
                    <input type="submit" value="Upload">
                </form>
            </body>
            </html>
            """
            
            self.wfile.write(form_html.encode('utf-8'))
        else:
            super().do_GET()

    def do_POST(self):
        content_type, _ = cgi.parse_header(self.headers['Content-Type'])
        
        if content_type == 'multipart/form-data':
            form_data = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD': 'POST'}
            )
            
            file_item = form_data['file']
            
            filename = os.path.join(os.getcwd(), file_item.filename)
            file_content = file_item.value
            
            with open(filename, 'wb') as f:
                f.write(file_content)
            
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'File uploaded successfully.')
        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b'Invalid content type')

if __name__ == "__main__":
    port = 8000
    Handler = FileUploadHandler
    httpd = socketserver.TCPServer(("", port), Handler)
    
    print(f"Serving on port {port} from the current working directory")
    httpd.serve_forever()
