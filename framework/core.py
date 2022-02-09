import main


class Application:
    def __init__(self, urlpatterns, front_controllers):
        self.urlpatterns = urlpatterns
        self.front_controllers = front_controllers
        self.ext_to_mime = {
            'bmp': 'bmp',
            'ico': 'x-icon',
            'gif': 'gif',
            'jpg': 'jpeg',
            'jpeg': 'jpeg',
            'jpe': 'jpeg',
            'tif': 'tiff',
            'tiff': 'tiff',
            'png': 'png',
            'cmd': 'cmd',
            'css': 'css',
            'csv': 'csv',
        }

    def __call__(self, environ, start_response):
        code, mime, file = '', '', ''
        path = environ['PATH_INFO']
        pos = path.rfind('.')
        if pos < 0:  # точка не найдена, значит не файл, а путь
            if path in self.urlpatterns:
                view = self.urlpatterns[path]
                request = {}
                for controller in self.front_controllers:
                    controller(request)
                code, text = view(request)
            else:
                view = self.urlpatterns['*']
                code, text = view()
            start_response(code, [('Content-Type', 'text/html')])
            return [text.encode('utf-8')]
        else:  # найдена точка? значит это файл, пытаемся определить какой
            extension = path[pos + 1:]
            f_name = path[path.rfind('/') + 1:]
            match extension:
                case 'css' | 'csv' | 'cmd':
                    mime = 'text/' + self.ext_to_mime[extension]
                    file = main.folders_tree['static'] + f_name
                    code = '200 OK'
                case 'bmp' | 'ico' | 'gif' | 'jpg' | 'jpeg' | 'jpe' | 'tif' | 'tiff' | 'png':
                    mime = 'image/' + self.ext_to_mime[extension]
                    file = main.folders_tree['pictures'] + f_name
                    code = '200 OK'
                case '_':
                    mime = ''
                    file = ''
                    code = '404 NOT FOUND'

            start_response(code, [('Content-Type', mime)])
            with open(file, 'rb') as f:
                content = f.read()
            return [content]
