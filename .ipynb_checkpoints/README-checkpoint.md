# Asset-Backed-Security-Modeling
ScriptUni Python in Finance Certificate Final Project
![certificate](python_certificate.png)

----------------------

## Summary
* [ABS background and purpose](#abs-background-purpose)
* [ABS model implementation]((#abs-implementation))

### ABS background
Every `structured deal` consists of a pool of `assets` (the `Loans`) and a group of `liabilities` (the *asset-backed securities*). The objective of structuring is to create and sell customized `securities` to investors, which are backed by the `pool of loans`.

### ABS model implementation

#### The waterfall 
Implement the actual asset-backed securities (the *liabilities*) in addition to the **Waterfall** mechanism that calculates the *cashflows* at each time period. The objective is to create well-designed `tranche` classes which will seamlessly work with your existing `Loan` classes. The outcome is to be able to take an input CSV of `loan data` and output a CSV with the all the `cashflows` at each time period (the *Waterfall*)


#### Waterfall metrics
Implement metrics on the **Waterfall**. This includes `Internal Rate of Return (IRR)`, `Reduction in Yield (DIRR)`, and `Average Life (AL)`. The objective and outcome is to be able to calculate and provide useful metrics on the structure.

#### Valuing the structure 
The last part is to value and rate the ABS. This entails creating a **Monte Carlo simulation** to simulate thousands of different *credit default* scenarios, all of which help determine the rating of the structure. The objective here is to get a taste of implementing an actual Monte Carlo simulation for finance in Python, utilizing the existing classes, **random number generation** and **multiprocessing**. The outcome will be a `rate`, `rating`, and `Weighted Average Life (WAL)` for each *tranche* of our very simple structure.
























