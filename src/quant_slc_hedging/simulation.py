from quant_slc_hedging.data_model import LoanModelInputs, SalaryModelInputs, SalaryGrowthType, salary_growth_amounts
from quant_slc_hedging.salary import SalaryModel
from quant_slc_hedging.loan import LoanModel
from quant_slc_hedging.strategies.min_repayment import MinRepaymentStrategy
import numpy as np 
import pandas as pd
from typing import List

# One SimHandler run performs n_paths sims for a salary config an strategy

stategy_types = List[MinRepaymentStrategy]

class SimulationHandler:
    def __init__(self, salary_config: SalaryModelInputs, loan_config: LoanModelInputs, strategy: stategy_types, n_paths: int, observations: int, seed: int) -> None:
        self.salary_config = salary_config
        self.loan_config = loan_config
        self.strategy = strategy
        self.n_paths = n_paths
        self.observations = observations
        rng = np.random.default_rng(seed)
        self.salary_model = SalaryModel(salary_config, rng)
        self.loan_model = LoanModel(loan_config)
        self.strategy_instance = strategy(salary_model=self.salary_model, loan_model=self.loan_model)

    def run_simulation(self):
        salary_paths = self.salary_model.generate_salary_paths(n_paths=self.n_paths, n_months=self.observations)
        loan_balance = np.zeros((self.n_paths, self.observations), dtype=float)
        interest_accrued = np.zeros((self.n_paths, self.observations), dtype=float)
        base_repayment = np.zeros((self.n_paths, self.observations), dtype=float)
        loan_balance[:, 0] = self.loan_config.initial_loan_balance
        additional_payments = np.zeros((self.n_paths, self.observations), dtype=float)

        for obs in range(1, self.observations):
            salary = salary_paths[:, obs]
            prev_loan_balance = loan_balance[:, obs-1]
            additional_payment = additional_payments[:, obs]

            additional_payment = self.strategy_instance.repayment_decision(
                salary=salary,
                loan_balance=prev_loan_balance,
            )

            loan_result = self.loan_model.calculate_obs(prev_loan_balance=prev_loan_balance, salaries=salary, additional_repayment=additional_payment)

            # TODO
            # action = self.strategy(loan_result)

            # Update arrays for next obs
            loan_balance[:, obs] = loan_result.loan_balance
            interest_accrued[:, obs] = loan_result.interest_accrued
            base_repayment[:, obs] = loan_result.base_repayment
        
        print("Sim finished")



if __name__ == "__main__":
    n_paths = 10_000
    years_remaining = 30
    observations = years_remaining * 12
    seed = 1234
    starting_salary = 35_000
    initial_loan = 45_000
    salary_growth = SalaryGrowthType(growth_type="Medium")
    salary_config=SalaryModelInputs(
        starting_salary=starting_salary,
        salary_growth_dist=salary_growth
        )
    loan_config = LoanModelInputs(
        initial_loan_balance=initial_loan,
        remaining_loan_term_months=12*years_remaining
    )
    sim = SimulationHandler(salary_config=salary_config, loan_config=loan_config, strategy=MinRepaymentStrategy, n_paths=n_paths, observations=observations, seed=seed)
    sim.run_simulation()