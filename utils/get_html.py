import os


def get_email(file_name):
    base_path = os.path.dirname(__file__)
    file_path = os.path.join(base_path, '../email_templates', file_name)
    with open(file_path, 'r') as file:
        return file.read()
