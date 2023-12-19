import http.server
import socketserver
import os
import re


class FileUploadHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Check if the request is for the form
        if self.path == '/upload_form':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            # HTML form for file upload
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
            # Serve files as usual
            super().do_GET()

    def do_POST(self):
        # Parse the Content-Length header
        content_length = int(self.headers['Content-Length'])
        
        # Read the POST data
        post_data = self.rfile.read(content_length)
        
        # Get the filename from the Content-Disposition header
        #filename = self.headers['Content-Disposition'].split('"')[1]
        filename = re.search(r'filename="([^"]+)"', str(post_data)).group(1)

        
        # Combine the filename with the current working directory
        filepath = os.path.join(os.getcwd(), filename)
        
        # Write the POST data to the file
        with open(filepath, 'wb') as f:
            f.write(post_data)
        
        # Send a response back to the client
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'File uploaded successfully.')

if __name__ == "__main__":
    port = 8000
    
    Handler = FileUploadHandler
    
    httpd = socketserver.TCPServer(("", port), Handler)
    
    print(f"Serving on port {port} from the current working directory")
    httpd.serve_forever()
