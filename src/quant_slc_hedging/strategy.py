from quant_common.statistics.basic_stats import sharpe_ratio

def example():
    returns = [0.01, 0.02, -0.005, 0.015]
    return sharpe_ratio(returns)


if __name__ == "__main__":
    print(example())