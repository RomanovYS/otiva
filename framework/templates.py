from jinja2 import Environment, FileSystemLoader


def render(path='', template='', **kwargs):
    with open(path + template, encoding='utf-8') as f:
        template = Environment(loader=FileSystemLoader(path)).from_string(f.read())
    return template.render(**kwargs)
