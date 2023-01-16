from .. import Solution, WeightSet
from ..model import Offline
from .online import NextFit as Nf_online
from .online import BestFit as Bf_online
from .online import FirstFit as Ff_online
from .online import WorstFit as Wf_online


class NextFit(Offline):

    def _process(self, capacity: int, weights: WeightSet) -> Solution:
        '''An offline version of NextFit, ordering the weight stream and
        delegating to the online version (avoiding code duplication)'''
        weights = sorted(weights, reverse=True)
        delegation = Nf_online()
        return delegation((capacity, weights))


class BestFit(Offline):

    def _process(self, capacity: int, weights: WeightSet) -> Solution:
        '''An offline version of BestFit, ordering the weight stream and
        delegating to the online version (avoiding code duplication)'''
        weights = sorted(weights, reverse=True)
        # print(weights)
        delegation = Bf_online()
        return delegation((capacity, weights))


class FirstFit(Offline):

    def _process(self, capacity: int, weights: WeightSet) -> Solution:
        '''An offline version of FirstFit, ordering the weight stream and
        delegating to the online version (avoiding code duplication)'''
        weights = sorted(weights, reverse=True)
        # print(weights)
        delegation = Ff_online()
        return delegation((capacity, weights))


class WorstFit(Offline):

    def _process(self, capacity: int, weights: WeightSet) -> Solution:
        '''An offline version of WorstFit, ordering the weight stream and
        delegating to the online version (avoiding code duplication)'''
        weights = sorted(weights, reverse=True)
        delegation = Wf_online()
        return delegation((capacity, weights))