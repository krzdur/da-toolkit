import numpy as np
import pandas as pd
import statsmodels.stats.api as sms
from statsmodels.stats.proportion import proportions_ztest
from scipy.stats import ttest_ind_from_stats


class Analysis:

    def __init__(self, df, metrics, variances=None, total_col='total_users', variant_col='variant', kind='prop',
                 alpha=0.05):
        self.df = df
        self.metrics = metrics
        self.variances = variances
        self.total_col = total_col
        self.variant_col = variant_col
        self.alpha = alpha

        self.variants = None
        self.sort_df()
        self.get_variants()

        self.results = {}
        self.results_df = None
        self.kind = kind
        self.run()

    def sort_df(self):
        self.df.sort_values(by=self.variant_col, inplace=True)

    def get_variants(self):
        variants = self.df[self.variant_col].values  # takes values from variant col
        variants.sort()
        self.variants = np.delete(variants, 0)  # removes 0 from variants

    def extract_variances(self):
        # if the list of variance columns is not provided assumes columns with 'var_' preffix
        if self.variances:
            assert len(self.metrics) == len(self.variances)
        else:
            self.variances = []
            for metric_name in self.metrics:
                var = 'var_' + metric_name
                self.variances.append(var)

    def test_prop(self, metric):
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

    def test_mean(self, metric, variance):
        self.results[metric] = {}
        for var in self.variants:
            temp_df = self.df[self.df[self.variant_col].isin(['0', var])]
            temp_df.set_index(self.variant_col, inplace=True)

            n1 = temp_df.loc['0', self.total_col]
            mean1 = temp_df.loc['0', metric]
            var1 = temp_df.loc['0', variance]
            std1 = np.sqrt(var1)

            n2 = temp_df.loc[var, self.total_col]
            mean2 = temp_df.loc[var, metric]
            var2 = temp_df.loc[var, variance]
            std2 = np.sqrt(var2)

            # run t-test
            t_stat, p_val = ttest_ind_from_stats(mean1=mean1, std1=std1, nobs1=n1,
                                                 mean2=mean2, std2=std2, nobs2=n2)

            # delta
            delta = mean2 / mean1 - 1

            # TODO power calc
            # es = sms.proportion_effectsize(cvr.iloc[1], cvr.iloc[0])  # Cohen's h
            # nobs1 = nobs.iloc[0]
            # ratio = nobs.iloc[1] / nobs.iloc[0]
            # power = sms.NormalIndPower().solve_power(es, nobs1=nobs1, alpha=self.alpha, ratio=ratio,
            #                                          alternative='two-sided')

            # display results
            if p_val > self.alpha:
                res = 'not significant'
            else:
                res = 'significant!'

            self.results[metric][var] = {'mean': [mean1, mean2],
                                         'delta': delta,
                                         't_stat': t_stat,
                                         'p_val': p_val,
                                         # 'power': power,
                                         'res': res
                                         }

    def save_to_df(self):
        reform = {(outerKey, innerKey): values for outerKey, innerDict in self.results.items() \
                  for innerKey, values in innerDict.items()}
        self.results_df = pd.DataFrame(reform).transpose()

    def run(self):
        if self.kind == 'prop':
            for metric in self.metrics:
                self.test_prop(metric)
        elif self.kind == 'mean':
            self.extract_variances()
            for metric, variance in zip(self.metrics, self.variances):
                self.test_mean(metric, variance)

        self.save_to_df()
        return self.results_df
