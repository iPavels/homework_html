from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs


class ShopHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        """Обрабатывает GET-запросы — возвращает страницу контактов"""
        if self.path == '/' or self.path == '/contacts':
            self._serve_html('contacts.html', 200)
        elif self.path == '/index':
            self._serve_html('index.html', 200)
        else:
            self._serve_html('404.html', 404)

    def do_POST(self):
        """Обрабатывает POST-запросы — выводит данные формы в консоль"""
        if self.path == '/contacts':
            # Читаем тело запроса
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')

            # Парсим данные формы
            data = parse_qs(body)

            # Выводим данные в консоль
            print('\n=== Новое сообщение с формы Контакты ===')
            for key, value in data.items():
                print(f'{key}: {value[0]}')
            print('=========================================\n')

            # Возвращаем страницу контактов с подтверждением
            self._serve_html('contacts.html', 200)
        else:
            self._serve_html('404.html', 404)

    def _serve_html(self, filename: str, status_code: int):
        """Читает HTML-файл и отправляет его клиенту"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()

            self.send_response(status_code)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(content.encode('utf-8'))

        except FileNotFoundError:
            # Если файл не найден — возвращаем простую 500 страницу
            error_html = '''<!DOCTYPE html>
<html lang="ru">
<head><meta charset="UTF-8"><title>500 — Ошибка сервера</title>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="d-flex align-items-center justify-content-center" style="min-height:100vh;background:#f8f9fa">
<div class="text-center">
    <h1 class="display-1 fw-bold text-danger">500</h1>
    <p class="fs-4 text-muted">Внутренняя ошибка сервера</p>
    <a href="/" class="btn btn-primary">На главную</a>
</div>
</body></html>'''
            self.send_response(500)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(error_html.encode('utf-8'))

    def log_message(self, format, *args):
        """Логируем каждый запрос"""
        print(f'[{self.address_string()}] {format % args}')


if __name__ == '__main__':
    HOST = 'localhost'
    PORT = 8000

    server = HTTPServer((HOST, PORT), ShopHandler)
    print(f'Сервер запущен: http://{HOST}:{PORT}')
    print('Нажми Ctrl+C чтобы остановить\n')

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\nСервер остановлен.')
        server.server_close()