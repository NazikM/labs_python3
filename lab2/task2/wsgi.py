from wsgiref.simple_server import make_server
from urllib.parse import parse_qs
from datetime import date


def application(environ, start_response):
    response_body = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Title</title>
        </head>
        <body>
        <form method="post">
            x: <input type="text" name="x">
            y: <input type="text" name="y">
            <button type="submit">Submit</button>
        </form>
        </body>
        </html>
    """
    if environ['REQUEST_METHOD'].upper() == 'GET':
        print(environ['QUERY_STRING'])
        status = '200 OK'

        response_headers = [('Content-Type', 'text/html; charset=UTF-8'),
                               ('Content-Length', str(len(response_body)))]

        start_response(status, response_headers)
        return [response_body.encode('utf-8')]
    elif environ['REQUEST_METHOD'].upper() == 'POST':
        today = date.today().strftime("%d/%m/%Y")

        try:
            request_body_size = int(environ.get('CONTENT_LENGTH', 0))
        except (ValueError):
            request_body_size = 0
        request_body = environ['wsgi.input'].read(request_body_size)
        data = parse_qs(request_body.decode('utf-8'))
        print(data)
        try:
            response = str(int(data['x'][0]) + int(data['y'][0]))
        except ValueError:
            response = "Incorrect format."
        status = '200 OK'
        response_headers = [('Content-Type', 'text/html; charset=UTF-8'),
                               ('Content-Length', str(len(response_body)))]

        start_response(status, response_headers)
        print(response)
        return ["Result: ".encode('utf-8'), response.encode('utf-8'), f"<br>Date: {today}".encode('utf-8')]
    else:
        return False


with make_server('localhost', 8000, application) as server:
    print("Starting server on 127.0.0.1:8000")
    server.serve_forever()
