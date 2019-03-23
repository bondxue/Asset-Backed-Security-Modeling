''''
Purpose: This module contain runSimulationParallel() function
Update:  12/05/2018
Author: Mengheng
Date: 12/05/2018
'''
import numpy as np
from usefulFunctions.doWaterfall import doWaterfall
from simulation.runSimulation import runSimlutation
from usefulFunctions.timer import Timer
from loan.loan_pool import LoanPool
from tranche.structured_securities import StructuredSecurities
import multiprocessing
import numpy


# doWork function can be any function with any argument
def doWork(input, output):
    while (True):
        try:
            f, args = input.get(timeout=1)
            res = f(*args)
            output.put(res)
        except:
            output.put('Done')
            break


def runSimulationParallel(loan_pool, structured_securities, NSIM, num_processes):
    input_queue = multiprocessing.Queue()
    output_queue = multiprocessing.Queue()

    # add 20 runMC function items into input_queue
    for i in range(num_processes):
        input_queue.put((runSimlutation, (loan_pool, structured_securities, NSIM / num_processes)))
        # create 5 child processes
    for i in range(num_processes):
        p = multiprocessing.Process(target=doWork, args=(input_queue, output_queue))
        p.start()

    res = []  # result
    # return the result list
    while True:
        r = output_queue.get()
        if r != 'Done':
            r = np.array(r)
            res.append(r)
        else:
            break
    DIRR_AL_sum = 0
    for i in range(len(res)):
        DIRR_AL_sum += res[i]
    return DIRR_AL_sum / num_processes
