from quant_slc_hedging.data_model import LoanModelInputs, SalaryModelInputs, SalaryGrowthType
import numpy as np 
import pandas as pd
from typing import Tuple

config = SalaryModelInputs(
    starting_salary=50_000,
    starting_loan_balance=60_000,
    salary_growth_dist=SalaryGrowthType(growth_type='Medium')
)

# Model salary as S(t+1)=S(t)e^(mu + sigma * rand)

class SalaryModel:
    def __init__(self, config: SalaryModelInputs) -> None:
        self.config = config
        self.rng_seed = 1234
        # standard normal as we want [0,1]
        self.rng_gen = np.random.default_rng(self.rng_seed)

    def _generate_random_array(self, size: Tuple[int, int]) -> np.ndarray:
        return self.rng_gen.standard_normal(size).reshape(size)

    def _build_paths(self, random_grid: np.ndarray) -> np.ndarray:
        print('here')

    def generate_salary_paths(self, n_paths: int, n_months: int) -> np.ndarry:
        rand_grid = self._generate_random_array((n_paths, n_months - 1))
        salary_paths = self._build_paths(rand_grid)

        return salary_paths

if __name__ == '__main__':
    sm = SalaryModel(config)
    rng = sm.generate_salary_paths(1000, 30*12)