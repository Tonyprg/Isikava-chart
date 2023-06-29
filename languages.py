class Language:
    def __init__(self):
        self.language = 'russian'  
        self.texts = {
            'russian': {
                'eng_language': 'Английский язык',
                'ru_language': 'Русский язык',
                'team_name': 'Команда Sigma',
                'to_choose_chart_btn': 'Диаграммы',
                'to_settings_btn': 'Настройки',
                'exit_btn': 'Выход',
                'add_chart': 'Добавить диаграмму',
                'choose_chart': 'Выбрать диаграмму',
                'delete_chart': 'Удалить диаграмму',
                'back': 'Назад',
                'change_style': 'Изменить стиль',
                'change_language': 'Изменить язык',
                'dark_theme': 'Темная тема',
                'light_theme': 'Светлая тема',
                'view': 'Просмотр',
                'edit': 'Редактирование',
                'edit_header': 'Заголовок',
                'edit_content': 'Содержание',
                'edit_image': 'Изображение',
                'edit_date': 'Дата',
                'edit_priority': 'Приоритет',
                'edit_chart_style': 'Стиль диаграммы',
                'header': 'Заголовок',
                'content': 'Содержание',
                'date': 'Дата',
                'vertex_describe': 'Описание узла',
                'priority': 'Приоритет',
                'add_node': 'Добавить вершину',
                'del_node': 'Удалить вершину',
                'edit_chart_name': 'Имя диаграммы',
                'save': 'Сохранить',
                'edit_node': 'Редактировать узел',
                'edit_chart': 'Редактировать диаграмму',
                'node': 'Узел',
                'chart': 'Диаграмма',
                'styles': 'Стили',
                'image': 'Изображение',
                'empty': '-пусто-'

            },
            'english': {
                'eng_language': 'English language',
                'ru_language': 'Russian language',
                'team_name': 'Sigma Team',
                'to_choose_chart_btn': 'Charts',
                'to_settings_btn': 'Settings',
                'exit_btn': 'Exit',
                'add_chart': 'Add chart',
                'choose_chart': 'Choose chart',
                'delete_chart': 'Delete chart',
                'back': 'Back',
                'change_style': 'Change style',
                'change_language': 'Change language',
                'dark_theme': 'Dark theme',
                'light_theme': 'Light theme',
                'view': 'View',
                'edit': 'Edit',
                'edit_header': 'Header',
                'edit_content': 'Content',
                'edit_image': 'Image',
                'edit_date': 'Date',
                'edit_priority': 'Priority',
                'edit_chart_style': 'Chart style',
                'header': 'Header',
                'content': 'Content',
                'date': 'Date',
                'vertex_describe': 'Vertex describe',
                'priority': 'Priority',
                'add_node': 'Add node',
                'del_node': 'Delete node',
                'edit_chart_name': 'Change chart name',
                'save': 'Save',
                'edit_node': 'Edit node',
                'edit_chart': 'Edit chart',
                'node': 'Node',
                'chart': 'Chart',
                'styles': 'Styles',
                'image': 'Image',
                'empty': '-empty-'
            }
        }

    def set_language(self, language):
        self.language = language

    def get_text(self, key):
        return self.texts[self.language][key]


