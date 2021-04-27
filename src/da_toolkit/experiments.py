import numpy as np
import pandas as pd
import statsmodels.stats.api as sms
from statsmodels.stats.proportion import proportions_ztest


class Analysis:

    def __init__(self, df, metrics, total_col='total_users', variant_col='variant', alpha=0.05):
        self.df = df
        self.metrics = metrics
        self.total_col = total_col
        self.variant_col = variant_col
        self.alpha = alpha

        self.variants = None
        self.sort_df()
        self.get_variants()

        self.results = {}
        self.results_df = None
        self.run()

    def sort_df(self):
        self.df.sort_values(by=self.variant_col, inplace=True)

    def get_variants(self):
        variants = self.df[self.variant_col].values  # takes values from variant col
        variants.sort()
        self.variants = np.delete(variants, 0)  # removes 0 from variants

    def test_metric(self, metric):
        self.results[metric] = {}
        for var in self.variants:
            temp_df = self.df[self.df[self.variant_col].isin(['0', var])]

            # t-test
            count = temp_df[metric]
            nobs = temp_df[self.total_col]
            z_stat, p_val = proportions_ztest(count, nobs)

            # cvr
            cvr = count / nobs
            cvr = cvr.reset_index(drop=True)

            # delta
            delta = cvr.iloc[1] / cvr.iloc[0] - 1

            # power calc
            es = sms.proportion_effectsize(cvr.iloc[1], cvr.iloc[0])  # Cohen's h
            nobs1 = nobs.iloc[0]
            ratio = nobs.iloc[1] / nobs.iloc[0]
            power = sms.NormalIndPower().solve_power(es, nobs1=nobs1, alpha=self.alpha, ratio=ratio,
                                                     alternative='two-sided')

            # display results
            if p_val > self.alpha:
                res = 'not significant'
            else:
                res = 'significant!'

            self.results[metric][var] = {'cvr': cvr,
                                         'delta': delta,
                                         'z_stat': z_stat,
                                         'p_val': p_val,
                                         'power': power,
                                         'res': res
                                         }

    def save_to_df(self):
        reform = {(outerKey, innerKey): values for outerKey, innerDict in self.results.items() \
                  for innerKey, values in innerDict.items()}
        self.results_df = pd.DataFrame(reform).transpose()

    def run(self):
        for metric in self.metrics:
            self.test_metric(metric)
        self.save_to_df()
        return self.results_df
