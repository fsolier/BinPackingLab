from .. import Solution, WeightStream
from ..model import Online


class NextFit(Online):

    def _process(self, capacity: int, stream: WeightStream) -> Solution:
        bin_index = 0
        solution = [[]]
        remaining = capacity
        for w in stream:

            if remaining >= w:
                solution[bin_index].append(w)
                remaining = remaining - w
            else:
                bin_index += 1
                solution.append([w])
                remaining = capacity - w
        return solution


class TerribleFit(Online):

    def _process(self, capacity: int, stream: WeightStream) -> Solution:
        solution = []
        for w in stream:
            solution.append(w)
        return solution 


class FirstFit(Online):

    def _process(self, capacity: int, stream: WeightStream) -> Solution:
        bin_size = 0
        bin_remainder = []
        solution = [[]]

        for w in stream:
            j = 0
            bin_remainder.append(0)  # adds 0 to remainder list = length of stream
            while (j < bin_size):
                if (bin_remainder[j] >= w):
                    bin_remainder[j]-=w
                    solution[j+1].append(w)
                    break
                j+=1

            if (j == bin_size):
                bin_remainder[bin_size] = capacity - w
                solution.append([w])
                bin_size += 1
            # print(bin_remainder)
        solution.pop(0)
        return solution


class BestFit(Online):
    
    def _process(self, capacity: int, stream: WeightStream) -> Solution:
        bin_size = 0
        solution = [[]]
        bin_remainder = []

        for w in stream:
            j = 0
            bin_remainder.append(0)
            min_space = capacity + 1  # init minimum space left
            bin_index = 0  # index of best bin with tightest spot

            for j in range(bin_size):
                if (bin_remainder[j] >= w and bin_remainder[j] - w < min_space):
                    bin_index = j
                    min_space = bin_remainder[j] - w

            if (min_space == capacity + 1):
                bin_remainder[bin_size] = capacity - w
                bin_size+=1
                solution.append([w])
            else:
                bin_remainder[bin_index] -= w
                solution[bin_index+1].append(w)
        solution.pop(0)
        return solution


class WorstFit(Online):
    
    def _process(self, capacity: int, stream: WeightStream) -> Solution:
        bin_size = 0
        solution = [[]]
        bin_remainder = []

        for w in stream:
            bin_remainder.append(0)
            max_space = -1  #  max space left
            bin_index = 0  # index of worst bin with max space

            for j in range(bin_size):
                if (bin_remainder[j] >= w and bin_remainder[j] - w > max_space):
                    bin_index = j
                    max_space = bin_remainder[j] - w

            if (max_space == -1):
                bin_remainder[bin_size] = capacity - w
                bin_size += 1
                solution.append([w])
            else:
                bin_remainder[bin_index] -= w
                solution[bin_index+1].append(w)
        solution.pop(0)

        return solution


class RefinedFirstFit(Online):

    def _process(self, capacity: int, stream: WeightStream) -> Solution:
        # A piece in (1/2, 1]
        A1 = int(capacity/2) + 1
        A2 = capacity
        # B1 piece in (2/5, 1/2]
        Bx1 = int(capacity*(2/5)) + 1
        Bx2 = int(capacity/2)
        # B2 piece in (1/3, 2/5]
        By1 = int(capacity/3) + 1
        By2 = int(capacity*(2/5))
        # X piece in (0, 1/3]
        X1 = 0
        X2 = int(capacity/3)
        Class1 = []
        Class2 = []
        Class3 = []
        Class4 = []
        temp_solution = []
        solution = []
        delegation = FirstFit()
        for w in stream:
            if (w >= A1 and w <= A2):
                Class1.append(w)
            if (w >= Bx1 and w <= Bx2):
                Class2.append(w)
            if (w >= By1 and w <= By2):
                # checks if w is the mk^th B2 piece
                if (w % 6 == 0 or w % 7 == 0 or w % 8 == 0 or w % 9 == 0):   
                    Class1.append(w)
                else:
                    Class3.append(w)
            if (w >= X1 and w <= X2):
                Class4.append(w)
        temp_solution.append(delegation((capacity, Class1)))
        temp_solution.append(delegation((capacity, Class2)))
        temp_solution.append(delegation((capacity, Class3)))
        temp_solution.append(delegation((capacity, Class4)))
        for i in temp_solution:
            for j in i:
                solution.append(j)

        return solution


class ConstantNumBins(Online):

    def _process(self, capacity: int, stream: WeightStream) -> Solution:
        solution = [[]]
        bin_size = []
        bin_remainder = []

        for w in stream:
            j = 0
            max_space = -1
            bin_index = 0
            min_space = capacity + 1
            while (j < bin_size):
                if (bin_remainder[j] >= w and bin_remainder[j] - w > max_space):
                    max_space = bin_remainder[j]-w
                if (bin_remainder[j] >= w and bin_remainder[j] - w < min_space):
                    min_space = bin_remainder[j] - w
            sum = max_space - min_space

            if (sum == 0):
                bin_remainder[bin_size] = capacity - w
                bin_size += 1
                solution.append([w])
            else:
                bin_remainder[bin_index] -= w
                solution[bin_index+1].append(w)
        return solution
