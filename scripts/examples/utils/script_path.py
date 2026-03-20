import os

path = os.path.join(os.getcwd(), '..')
output_file_name = f'{path}/output_docs/test.txt'
with open(output_file_name, 'w') as out:
    out.write('1')
    out.close()
