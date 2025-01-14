import tensorflow as tf
import numpy as np
from tensorflow.keras.utils import Sequence

#x data is np memmap, so that it can be loaded
#y data is np memmap for similarity

ada_x_mmap = np.load('./adasyn/x_ecfpada.npy', mmap_mode='r')
ada_y_mmap = np.load('./adasyn/y_ecfpada.npy', mmap_mode='r')

# batch_size = 30000
# dim = ada_x_mmap.shape
# classes = 2

class data_generator(Sequence):

    # def __init__(self, list_IDs, labels, dim, batch_size=32, n_channels=1,
    #              n_classes=2, shuffle=True):
    
    def __init__(self, x_set, y_set, batch_size, shuffle=True):
        'Initialisation'
        # self.dim = dim
        self.batch_size = batch_size
        self.x_data = x_set
        self.y_data = y_set
        # self.labels = labels
        self.datalen = len(y_set)
        self.indexes = np.arange(self.datalen)

        # self.list_IDs = range(0, len(self.x_data))
        self.shuffle = shuffle
        self.on_epoch_end()

    def __len__(self):
        return int(np.ceil(self.datalen / self.batch_size))

    def __getitem__(self, index):
        'Generate one batch'
        indexes = self.indexes[index*self.batch_size : (index+1)*self.batch_size]

        # tmp_list_IDs = [self.list_IDs[k] for k in indexes]

        x_batch = self.x_data[indexes]
        y_batch = self.y_data[indexes]

        #generate data
        # x, y = self.__generate_data(tmp_list_IDs)

        return x_batch, y_batch

    def on_epoch_end(self):
        self.indexes = np.arange(self.datalen)

        if self.shuffle:
            np.random.shuffle(self.indexes)

    # def __generate_data(self, tmp_list_IDs):
    #     'generates the data in batch size samples'

    #     X = np.empty((self.batch_size, self.dim))
    #     Y = np.empty((self.batch_size), dtype=int)

    #     # print(self.x_data[0].shape)
    #     # print(X[0].shape)
    #     # print(X.shape)

    #     for ID, i in enumerate(tmp_list_IDs):
    #         X[ID] = self.x_data[i]
    #         Y[ID] = self.y_data[i]
            
    #         print(self.x_data[i])
    #         print(self.y_data[i])
    #         break


    #     return X, Y

# generator = data_generator(ada_x_mmap, ada_y_mmap, dim, batch_size, n_classes=classes)
