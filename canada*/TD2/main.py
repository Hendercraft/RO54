from math import sqrt


class Position:
    def __init__(self, coords: list):
        self.coords = coords

    @staticmethod
    def distance(p1, p2):
        dis = 0
        for i in range(0, 3):
            dis += pow(p1.coords[i] - p2.coords[i], 2)
        return sqrt(dis)


class Object:
    def __init__(self, rss: list):
        self.coords = (0, 0)
        self.fp = FingerPrint(rss)


class FingerPrint:
    def __init__(self, rss: list):
        self.rss = rss


class Cell:
    def __init__(self, position: list, fp: list):
        self.position = Position(position)
        self.fp = FingerPrint(fp)
        self.metric = 0

    def compute_metric(self, rss: list):
        for i in range(0, 4):
            self.metric += abs(self.fp.rss[i] - rss[i])


def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[0]
    left = []
    right = []
    for i in range(1, len(arr)):
        if arr[i].metric < pivot.metric:  # compare the metric of the cells
            left.append(arr[i])  # if lower add it to the left
        else:
            right.append(arr[i])  # else add it to the right
    return quicksort(left) + [pivot] + quicksort(right)


class GoFingerPrint:
    def __init__(self, cells: list, terminal: Object):
        self.cells = cells
        self.terminal = terminal
        self.kcells = []
        self.alphas = []

    def getKcells(self):
        templist = []
        for row in self.cells:  # Putting the list in 1D for the quicksort
            for cell in row:
                templist.append(cell)
        sorted_list = quicksort(templist)  # sorting the array to determine the cells with the lowest
        self.kcells = sorted_list[0:4]  # returning last 4 cells

    def compute_cells_metrics(self):
        for row in self.cells:
            for cell in row:
                cell.compute_metric(terminal.fp.rss)
                print(cell.position.coords)
                print(cell.metric)

    def compute_alpha(self):
        m1 = self.kcells[0].metric
        m2 = self.kcells[1].metric
        m3 = self.kcells[2].metric
        m4 = self.kcells[3].metric

        alpha1 = 1. / (1 + m2 / m1 + m3 / m1 + m4 / m1)
        alpha2 = m2 / m1 * alpha1
        alpha3 = m3 / m1 * alpha1
        alpha4 = m4 / m1 * alpha1
        self.alphas = [alpha1, alpha2, alpha3, alpha4]

    def compute_terminal_estimate(self):
        x = 0
        y = 0
        for i in range(0, 4): # OM = alpha1*Oc1 + alpha2*Oc2 + alpha3*Oc3 + alpha4*Oc4
            x += (self.alphas[i] * self.kcells[i].position.coords[0])
            y += (self.alphas[i] * self.kcells[i].position.coords[1])
        self.terminal.coords = (x, y)

    def Master(self):
        self.compute_cells_metrics()
        self.getKcells()
        self.compute_alpha()
        self.compute_terminal_estimate()
        print("the terminal coords are : ")
        print(self.terminal.coords)
        print("Our alpha are : ")
        print(self.alphas)


cells_list = [
    [Cell([2, 2], [-38, -17, -54, -13]), Cell([6, 2], [-34, -27, -38, -41]), Cell([10, 2], [-17, -50, -44, -33])],
    [Cell([2, 6], [-74, -62, -48, -33]), Cell([6, 6], [-64, -48, -72, -35]), Cell([10, 6], [-27, -28, -32, -45])],
    [Cell([2, 10], [-19, -28, -12, -40]), Cell([6, 10], [-45, -37, -20, -15]), Cell([10, 10], [-30, -20, -60, -40])],
]

terminal = Object([-26, -42, -13, -46])

Go = GoFingerPrint(cells_list, terminal)
Go.Master()
