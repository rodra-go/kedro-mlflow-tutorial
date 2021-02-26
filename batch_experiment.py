import subprocess


BASE_CMD = '/home/user01/.local/bin/kedro run --pipeline ds --params regressor.hyperp.kernel:{}'
VALUES = ['linear', 'poly', 'rbf', 'sigmoid']

print('Starting batch experiment...')
for value in VALUES:
    BASE_CMD.format(value)
    print('CMD: {}'.format(BASE_CMD.format(value)))
    process = subprocess.run(BASE_CMD.format(value).split(' '))
    # process = subprocess.run(['pwd'])
    print('Running CMD...')
    print('Done!')
