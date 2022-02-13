from pprint import pprint

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

    def to_path_go(self, path, start_response):
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

    def __call__(self, environ, start_response):
        code, mime, file = '', '', ''
        path = environ['PATH_INFO']
        if environ['REQUEST_METHOD'] == 'GET':
            pos = path.rfind('.')
            if pos < 0:  # точка не найдена, значит не файл, а путь
                return self.to_path_go(path, start_response)
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
        elif environ['REQUEST_METHOD'] == 'POST':
            content = environ['wsgi.input'].read(int(environ['CONTENT_LENGTH'])).decode('utf-8')
            param_list = content.split('&')
            param_dict = {}
            for param in param_list:
                key, val = param.split('=')
                param_dict[key] = val
            print(param_dict)  # выводим словарь параметров
            return self.to_path_go(path, start_response)
        else:
            print('Unknown method')
            return self.to_path_go(path, start_response)
