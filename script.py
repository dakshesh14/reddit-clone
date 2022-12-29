import os


def delete_migrations():
    # NOTE: This script will delete all migrations files in the project.
    # Migrations files are used to keep track of database changes.
    # If you want to delete all migrations files, run this script.
    # If you want to delete a specific migrations file, delete it manually.
    sure = input(
        'Are you sure you want to delete all migrations files? (y/n) ')
    if sure != 'y':
        return
    for root, dirs, files in os.walk('.'):
        # ignore .env and .git
        if '.env' in root or '.git' in root:
            continue
        if 'migrations' in dirs:
            migrations_path = os.path.join(root, 'migrations')
            for file in os.listdir(migrations_path):
                if file != '__init__.py':
                    os.remove(os.path.join(migrations_path, file))
                    print('Deleted migrations file: {}'.format(file))


if __name__ == '__main__':
    delete_migrations()
