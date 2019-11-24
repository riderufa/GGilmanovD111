import sys
import requests

auth_params = {
    'key': "f9c57c8081616ebea6d84381be5074d5",
    'token': "ff5b24df72c5fcddac20b72b77342d6c8526afedad9e50d9106bcae6e0861991", }

base_url = "https://api.trello.com/1/{}"

board_id = "YNLBxrxd"

def read():
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()
    # print(column_data)
    for column in column_data:
        task_data = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()
        print(column['name'] + ' - Количество задач: {}'.format(len(task_data)))
        if not task_data:
            print('\t' + 'Нет задач!')
            continue
        for task in task_data:
            print('\t' + task['name'] + ' - ID ' + task['id'])
    print(len(double_task("Изучить Python")))

def double_task(name):
    tasks_list = {}
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()
    for column in column_data:
        column_tasks = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()
        for task in column_tasks:
            if task['name'] == name:
                tasks_list[column['name']] = task
    return tasks_list


def create(name, column_name):
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()
    for column in column_data:
        if column['name'] == column_name:
            requests.post(base_url.format('cards'), data={'name': name, 'idList': column['id'], **auth_params})
            break

def create_column(column_name):
    response = requests.get(base_url.format('boards/' + board_id), params=auth_params).json()
    board_id1 = response['id']
    requests.post(base_url.format('lists'), data={'name': column_name, 'idBoard': board_id1, **auth_params})
    
        
def move(name, column_name):
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()
    double_task_list = double_task(name)
    task_id = None
    # for column in column_data:
        # column_tasks = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()
        # for task in column_tasks:
            # if task['name'] == name:
    if len(double_task_list) > 1:
        print('Задач с именем {} больше одной:'.format(name))
        for key in double_task_list:
            print('Задача {} с ID {} в колонке {}.'.format(double_task_list[key]['name'], double_task_list[key]['id'], key)) 
        task_id = input('Введите ID выбранной задачи: ')
    else:
        for key in double_task_list:
            task_id = double_task_list[key]['id']
                    # break
        # if task_id:
            # break
    for column in column_data:
        if column['name'] == column_name:
            requests.put(base_url.format('cards') + '/' + task_id + '/idList', data={'value': column['id'], **auth_params})
            break

if __name__ == "__main__":
    if len(sys.argv) <= 2:
        read()
    elif sys.argv[1] == 'create':
        create(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == 'createcolumn':
        create_column(sys.argv[2])
    elif sys.argv[1] == 'move':
        move(sys.argv[2], sys.argv[3])