#Данные JSON
import json
#Работа с файлами
import os
#
import uuid
#
import sys
# if sys.version_info[1]>12:
#     import legacy-cgi
# else:
import cgi
# логирование
import logging
#Сервер
from http.server import BaseHTTPRequestHandler
#То, что надо из конфигурации
from configuration import get_paths, check_image, secure_filename, get_extension
#Библиотека изображений
from PIL import Image

#Сервер картинок
class ImageServer(BaseHTTPRequestHandler):
    # Запрос GET
    def do_GET(self):
        if self.path == '/':
            self.serve_file('static/index.html', 'text/html')
            logging.info('Main page accessed')
        elif self.path == '/upload':
            self.serve_file('static/upload.html', 'text/html')
            logging.info('Upload page accessed')
        elif self.path == '/images':
            self.serve_images_list()
            logging.info('Images list accessed')
        else:
            self.send_error(404, 'Not Found')

    # Запрос POST
    def do_POST(self):
        if self.path == '/upload':
            try:
                # Parse multipart form data
                content_type = self.headers.get('content-type')
                if not content_type or 'multipart/form-data' not in content_type:
                    self.send_error_response(400, 'Invalid content type')
                    logging.error('Invalid content type')
                    return

                form = cgi.FieldStorage(
                    fp=self.rfile,
                    headers=self.headers,
                    environ={'REQUEST_METHOD': 'POST'}
                )

                if 'file' not in form:
                    self.send_error_response(400, 'No file part')
                    logging.error('No file part in request')
                    return

                file_item = form['file']
                if not file_item.filename:
                    self.send_error_response(400, 'No selected file')
                    logging.error('No selected file')
                    return

                state,err_msg = check_image(file_item.filename)
                if not state:
                    self.send_error_response(400, err_msg)
                    logging.error(f'Error message for {file_item.filename} : {err_msg}')
                    return

                # Generate unique filename
                ext = get_extension(file_item.filename)
                unique_filename = f"{uuid.uuid4()}.{ext}"
                filename = secure_filename(unique_filename)
                upload_fldr = get_paths()[0]
                filepath = os.path.join(upload_fldr, filename)

                # Save file
                os.makedirs(upload_fldr, exist_ok=True)
                file_data = file_item.file.read()
                with open(filepath, 'wb') as f:
                    f.write(file_data)
                    os.chmod(filepath, 0o664)  # Ensure readable by Nginx
                logging.info(f'File saved to: {filepath}')  # Debug log

                # Verify image
                try:
                    Image.open(filepath).verify()
                except Exception as err:
                    os.remove(filepath)
                    self.send_error_response(400, 'Invalid image file')
                    logging.error(f'Invalid image file: {filename}, {err}')
                    return

                image_url = f"{upload_fldr}/{filename}"
                logging.info(f'Success: image {filename} uploaded')

                # Send success response
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {
                    'message': 'File uploaded successfully',
                    'filename': filename,
                    'url': image_url
                }
                self.wfile.write(json.dumps(response).encode('utf-8'))

            except Exception as e:
                self.send_error_response(500, f'Error saving file: {str(e)}')
                logging.error(f'Error saving file: {str(e)}')

        else:
            self.send_error(404, 'Not Found')

    # Запрос
    def serve_file(self, filepath, content_type):
        try:
            with open(filepath, 'rb') as f:
                self.send_response(200)
                self.send_header('Content-type', content_type)
                self.end_headers()
                self.wfile.write(f.read())
        except FileNotFoundError:
            self.send_error(404, 'Not Found')

    # Запрос списка rfhnbyjr
    def serve_images_list(self):
        try:
            upload_fldr = get_paths()[0]
            os.makedirs(upload_fldr, exist_ok=True)
            files = [f for f in os.listdir(upload_fldr) if check_image(f)]
            html = '<!DOCTYPE html><html><head><title>Uploaded Images</title></head><body>'
            html += '<h1>Uploaded Images</h1><ul>'
            for file in files:
                html += f'<li><a href="/images/{file}">{file}</a></li>'
            html += '</ul><p><a href="/">Back to home</a></p></body></html>'
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(html.encode('utf-8'))
        except Exception as e:
            self.send_error_response(500, f'Error listing images: {str(e)}')
            logging.error(f'Error listing images: {str(e)}')

    def send_error_response(self, code, message):
        self.send_response(code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"error": message}).encode('utf-8'))
