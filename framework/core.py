import main

categories_list = []
courses_dict = {}


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

    def mime_sel(self, path, pos):
        mime, file, code = '', '', ''
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
                code = '404 NOT FOUND'
        return code, mime, file

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

    def percent_coding(self, inline):
        inline = inline.replace('+',' ')
        while True:
            pos = inline.find('%')
            if pos < 0:
                return inline
            outline = inline[:pos]
            code = inline[pos + 1:pos + 3]
            outline += chr(int('0X' + code, 16))
            outline += inline[pos + 3:]
            inline = outline


    def parse_content(self, content):
        content = self.percent_coding(content)
        param_list = content.split('&')
        param_dict = {}
        for param in param_list:
            key, val = param.split('=')
            try:
                param_dict[key].append(val)
            except KeyError:
                param_dict[key] = []
                param_dict[key].append(val)
        return param_dict

    def post_processing(self, param_dict):
        keys = param_dict.keys()  # получаем ключи пришедшего словаря
        if 'new_category' in keys:
            name_cat = param_dict['new_category'][0]
            if name_cat and not name_cat in categories_list:
                categories_list.append(name_cat)  # добавляем в список доступных категорий
        elif 'new_course' in keys:
            key = param_dict['new_course'][0]
            if not key:
                return
            try:
                val = param_dict['category'] # если не выбрано ни одной категории, создаём пустой список
            except KeyError:
                val = []
            courses_dict[key] = val  # добавляем в словарь доступных курсов
        elif 'email' in keys:
            print('Контактные данные')
        else:
            print('Непонятно что')

    def __call__(self, environ, start_response):
        method = environ['REQUEST_METHOD']
        path = environ['PATH_INFO']
        pos = path.rfind('.')
        if method == 'GET':
            if pos < 0:  # точка не найдена, значит не файл, а путь
                return self.to_path_go(path, start_response)
            else:  # найдена точка? значит это файл, пытаемся определить какой
                code, mime, file = self.mime_sel(path, pos)
                start_response(code, [('Content-Type', mime)])
                with open(file, 'rb') as f:
                    content = f.read()
                return [content]
        elif method == 'POST':
            # получаем содержимое POST запроса
            content = environ['wsgi.input'].read(int(environ['CONTENT_LENGTH'])).decode('utf-8')
            param_dict = self.parse_content(content)  # разбираем содержимое на словарь
            self.post_processing(param_dict)  # обрабатываем словарь параметров
            return self.to_path_go(path, start_response)
        else:
            print('Unknown method')
            return self.to_path_go(path, start_response)
