import os

def get_text_from_file(file_path):
    if not os.path.exists(file_path):
        file = open(file_path, "w+")
        file.close()
    file = open(file_path, "r")
    f = file.read()
    file.close()

    return f

def input_text_to_file(file_path, text):
    if not os.path.exists(file_path):
        file = open(file_path, "w+")
        file.close()
    file = open(file_path, "w")
    file.write(text)
    file.close()

def get_settings():
    if get_text_from_file('settings'):
        settings = get_text_from_file('settings')
        settings = settings.split('\n')
        temp = dict()
        for line in settings:
            key = line.split('=')[0]
            value = line.split('=')[1]
            temp[key] = value
        return temp

def save_settings(sett_dict):
    if sett_dict:
        temp = ''
        for line in sett_dict.keys():
            temp = temp + line + '=' + sett_dict[line] + '\n'
        if temp:
            temp = temp[:-1]
        input_text_to_file('settings', temp)
