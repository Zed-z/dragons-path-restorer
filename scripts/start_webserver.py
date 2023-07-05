import webbrowser
import http.server
import socketserver
import os

def main():

    webserver_port = 8080

    webbrowser.open('http://localhost:' + str(webserver_port))

    web_dir = os.path.join(os.path.dirname(__file__), "../experience_restored")
    os.chdir(web_dir)

    print("Serving website at http://localhost:" + str(webserver_port))
    httpd = socketserver.TCPServer(("", webserver_port), http.server.SimpleHTTPRequestHandler)
    httpd.serve_forever()


if __name__ == '__main__':
    main()
