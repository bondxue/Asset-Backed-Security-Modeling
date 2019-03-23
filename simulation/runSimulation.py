''''
Purpose: This module contain simulateWaterfall function
Author: Mengheng
Date: 12/05/2018
'''
import numpy as np
from usefulFunctions.doWaterfall import doWaterfall
from loan.loan_pool import LoanPool
from tranche.structured_securities import StructuredSecurities


def runSimlutation(loan_pool, structured_securities, NSIM):
    num_tranches = len(structured_securities.tranche_list)
    # record sum of all DIRR and AL results and initialization with zeros
    sum_DIRR_AL_results = np.zeros((num_tranches, 2))
    # do waterfall and sum DIRR and AL of each simulation
    for i in xrange(NSIM):
        loan_pool.reset()
        structured_securities.reset()
        loan_pool_waterfall, structured_securities_waterfall, reserve_account_waterfall, tranche_metrics = doWaterfall(
            loan_pool, structured_securities)
        for j, tranche_metric in enumerate(tranche_metrics):
            if tranche_metric[2] != np.inf:  # if AL not infinite
                sum_DIRR_AL_results[j] += [tranche_metric[1], tranche_metric[2]]
            else:
                sum_DIRR_AL_results[j] += [tranche_metrics[1], 0]
    # return the average DIRR and WAL values for each tranche
    DIRR_AL = sum_DIRR_AL_results / NSIM
    DIRR_AL = DIRR_AL.tolist()
    return DIRR_AL
