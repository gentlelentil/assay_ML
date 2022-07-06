import numpy as np

with open('checkthisbullshit.txt') as bsfile:
    for i in bsfile:
        i = i.replace('\n', '')
        i = i.split(' ')
        for j in i:
            try:
                check = float(j)
                array = np.array(j, dtype=np.float32)
            except:
                print(j)