''''
Purpose: This module contain runMonte function
Update:  12/05/2018 use runSimulationParallel() instead of runSimulation()
Author: Mengheng
Date: 12/05/2018
'''

import numpy as np
from runSimulation import runSimlutation
from tranche.tranche_base import Tranche
from tranche.structured_securities import StructuredSecurities
from simulation.runSimulationParallel import runSimulationParallel


def runMonte(loan_pool, tranche_percents, tranche_rates, tranche_levels, coeffs, tolerance, NSIM, num_processes):
    diff = np.inf  # initialize diff
    rates = tranche_rates
    num_tranches = len(tranche_rates)
    DIRR_AL = np.zeros((num_tranches, 2))  # initialize DIRR and AL results
    while diff > tolerance:
        structured_securities = StructuredSecurities.constructSecurities(loan_pool.totalPrincipal(), tranche_percents,
                                                                 rates, tranche_levels)
        DIRR_AL = runSimulationParallel(loan_pool, structured_securities, NSIM, num_processes)
        yields = Tranche.calculateYield(DIRR_AL[:, 0], DIRR_AL[:, 1])
        new_rates = Tranche.newTrancheRate(rates, coeffs, yields)
        diff = Tranche.diff(tranche_percents, rates, new_rates)
        rates = new_rates
        print 'diff = {}'.format(diff)
    rates.shape = (len(rates), 1)  # change row vector to column vector
    Ratings = np.array([Tranche.ABSRating(dirr) for dirr in DIRR_AL[:, 0]])
    Ratings.shape = (len(Ratings), 1)  # change row vector to column vector
    # DIRR, WAL, rate, Rating of each tranche
    MC_matrics = np.hstack((DIRR_AL, rates, Ratings))
    return MC_matrics
