import pandas as pd 
from dataclasses import dataclass
from typing import Literal, List

@dataclass
class SalaryGrowthType:
    growth_type: Literal['High', 'Medium', 'Low'] = 'Medium'

@dataclass 
class SalaryModelInputs:
    starting_salary: float
    starting_loan_balance: float
    salary_growth_dist: SalaryGrowthType

@dataclass
class LoanModelInputs:
    loan_max_horizon_months: int = 30 * 12
    interest_growth: float = 0.03
    repayment_amount_pct: float = 0.09
    repayment_threshold: float = 28_470
    # repayment_strategies: List[float] = []