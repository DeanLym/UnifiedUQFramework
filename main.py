from CUQMain import *


class MyUQMain(UQMain):
    # def __init__(self):
    #     super(MyUQMain,self).__init__()

    def sim(self):
        print("My sim...")


if __name__ == "__main__":
    print("This is main.")
    main = MyUQMain()
    main.alg_ = UQAlg.EnS
    main.mpi_run = True
    main.solve()
