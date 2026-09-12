from quant_slc_hedging.data_model import LoanModelInputs, SalaryModelInputs, SalaryGrowthType, salary_growth_amounts
from quant_slc_hedging.salary import SalaryModel
from quant_slc_hedging.loan import LoanModel
import numpy as np 
import pandas as pd
from dataclasses import dataclass

class MinRepaymentStrategy:
    def __init__(self, salary_model: SalaryModel, loan_model: LoanModel) -> None:
        self.salary_model = salary_model
        self.loan_model = loan_model

    def repayment_decision(self, salary: np.ndarray, loan_balance: np.ndarray) -> np.ndarray:
        return np.zeros(shape=salary.shape)