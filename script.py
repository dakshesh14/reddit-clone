import os


def delete_migrations():
    sure = input(
        'Are you sure you want to delete all migrations files? (y/n) ')
    if sure != 'y':
        return
    for root, dirs, files in os.walk('.'):
        if 'migrations' in dirs:
            migrations_path = os.path.join(root, 'migrations')
            for file in os.listdir(migrations_path):
                if file != '__init__.py':
                    os.remove(os.path.join(migrations_path, file))
                    print('Deleted migrations file: {}'.format(file))


if __name__ == '__main__':
    delete_migrations()
