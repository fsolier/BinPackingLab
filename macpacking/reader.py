from abc import ABC, abstractmethod
from os import path
from random import shuffle, seed
from . import WeightSet, WeightStream


class DatasetReader(ABC):

    def offline(self) -> WeightSet:
        '''Return a WeightSet to support an offline algorithm'''
        (capacity, weights) = self._load_data_from_disk()
        seed(42)          # always produce the same shuffled result
        shuffle(weights)  # side effect shuffling
        return (capacity, weights)

    def online(self) -> WeightStream:
        '''Return a WeighStream, to support an online algorithm'''
        (capacity, weights) = self.offline()

        def iterator():  # Wrapping the contents into an iterator
            for w in weights:
                yield w  # yields the current value and moves to the next one

        return (capacity, iterator())

    @abstractmethod
    def _load_data_from_disk(self) -> WeightSet:
        '''Method that read the data from disk, depending on the file format'''
        pass


class BinppReader(DatasetReader):
    '''Read problem description according to the BinPP format'''

    def __init__(self, filename: str) -> None:
        if not path.exists(filename):
            raise ValueError(f'Unknown file [{filename}]')
        self.__filename = filename

    def _load_data_from_disk(self) -> WeightSet:
        with open(self.__filename, 'r') as reader:
            nb_objects: int = int(reader.readline()) #reads first line
            capacity: int = int(reader.readline()) #second line 
            weights = []
            for _ in range(nb_objects):
                weights.append(int(reader.readline()))
            return (capacity, weights)

class jburkardtReader(DatasetReader):
    def __init__(self, filename: str):
        if not path.exists(filename):
            raise ValueError(f'Unknown file [{filename}]')
        self.__filename = filename
    
    def _load_data_from_disk(self) -> WeightSet:
        weights = []
        optimal = []
        capacity = 0
        if '_c' in self.__filename:
            with open(self.__filename, 'r') as reader:
                capacity: int = int(reader.readline())
        if '_s' in self.__filename:
            with open(self.__filename, 'r') as reader:
                for _row in reader:
                    optimal.append(int(reader.readline()))
        elif '_w' in self.__filename:
            with open(self.__filename, 'r') as reader:
                for row in reader:
                    weights.append(int(row.strip()))
                    weights.append(int(reader.readline()))
        return (capacity, weights)
