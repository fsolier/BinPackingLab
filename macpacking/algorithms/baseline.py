from .. import Solution
from ..model import Offline
import binpacking as bp
import math


class BenMaier(Offline):

    def _process(self, capacity: int, weights: list[int]) -> Solution:
        return bp.to_constant_volume(weights, capacity)


class BenMaier2(Offline):

    def _process(self, capacity: int, weights: list[int]) -> Solution:
        sum = 0
        for i in weights:
            sum += i
        nb_bins = math.ceil(sum/capacity)  # returns lower bound of nb_bins
        return bp.to_constant_bin_number(weights, nb_bins)
