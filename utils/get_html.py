import os


def read_file(file_name):
    base_path = os.path.dirname(__file__)
    file_path = os.path.join(base_path, '../email_templates', file_name)
    with open(file_path, 'r') as file:
        return file.read()


def default_html(*, message, title):
    base_path = os.path.dirname(__file__)
    file_path = os.path.join(base_path, '../email_templates', "boilerplate.html")
    with open(file_path, 'r') as file:
        return file.read().replace("{{title}}", title).replace("{{message}}", message)
