from quant_slc_hedging.data_model import LoanModelInputs, SalaryModelInputs, SalaryGrowthType, salary_growth_amounts
from quant_slc_hedging.salary import SalaryModel
from quant_slc_hedging.loan import LoanModel
import numpy as np 
import pandas as pd
from dataclasses import dataclass

class FixedPctRepaymentStrategy:
    """Repayment strategy that pays a fixed % of salary each month if above threshold."""
    def __init__(self, fixed_excess_pct: float, repayment_threshold: float) -> None:
        self.fixed_excess_pct = fixed_excess_pct
        self.repayment_threshold = repayment_threshold

    def repayment_decision(self, salary: np.ndarray, loan_balance: np.ndarray) -> np.ndarray:
        """Returns a monthly additional repayment from an input annual salary."""
        salary_excess = np.maximum(0, salary - self.repayment_threshold)
        
        return salary_excess * self.fixed_excess_pct / 12.0