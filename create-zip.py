import shutil
import os

def create_zip():
    """
    # Creates zip of create-todo and read-todo
    This method creates zip of create-todo and read-todo lambdas and store the zip created inside a folder called 'zipped'
    """
    for filepath in ['create-todo', 'read-todo']:
        shutil.make_archive(f'./zipped/{filepath}', 'zip', f'./{filepath}/')
    print("Finished creating zip. Zip stored inside 'zipped' folder!!")

def generate_tree(startpath='.'):
    """
    # Generate Tree structure
    This method generates tree structure of current folder by default. We can generate tree of another folder by passing
    path as argument inside __main__ where method is called.
    """
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 2 * (level)
        print('{}|'.format(indent[:]))
        print('{}+{}/'.format(indent, os.path.basename(root)))
        subindent = ' ' * 2 * (level + 1)

        for f in files:
            print('{}| +--- {}'.format(subindent[:-2], f))

if __name__ == '__main__':
    create_zip()
    generate_tree()