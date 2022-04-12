import os

path = os.getcwd() + '/OST'
folder = 'Turning Red	'
folder = folder.strip()
folder = folder.replace(" ", "_")
print(path)
print('>>> ' + folder + ' ' + str(len(os.listdir(path))))
for file in os.listdir(path + '/' + folder):
    if file != '.spotdl-cache':
        print(file)
