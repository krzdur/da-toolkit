import scipy.stats
import string
import scipy

from typing import List # Typing
import numpy as np # Linear algebra
import pandas as pd # Data processing, CSV file I/O (e.g. pd.read_csv)
import re # Regular expressions for advanced string selection


class Analysis:
    def __init__(self, df: pd.DataFrame, group_by_cols: List[str], cols_to_analyze: List[str]):
        self.df = df
        self.group_by_cols = group_by_cols
        self.cols_to_analyze = cols_to_analyze

        self.result = {}
        self.analysis_types = []
        self.result_difference = {}
        self.device_types = []

    @staticmethod
    def gen_variants_dict(variants):
        variants_int = list(np.sort(variants.map(int).unique()))

        d = {v: 'Var {}'.format(string.ascii_uppercase[v - 1]) for v in variants_int if v > 0}
        d[0] = 'Control'
        return d

    @staticmethod
    def significance90(p_value: float) -> str:
        if p_value > 0.95 or p_value < 0.05:
            return "Yes"
        else:
            return "No"

    @staticmethod
    def significance95(p_value: float) -> str:
        if p_value > 0.975 or p_value < 0.025:
            return "Yes"
        else:
            return "No"

    # Send a df  with raw values and create a df_CVR with conversion rates for the given parameters below
    # The function still does not account for multi-index df
    def generate_cvrs(self, group_by_cols: List[str]) -> pd.DataFrame:
        df_gb = self.df.groupby(group_by_cols).sum()
        self.df_CVRs = df_gb.reset_index().copy()

        # averages
        self.df_CVRs["avgPageviewsPerUser"] = self.df_CVRs.totalPageviews / self.df_CVRs.uniqueUsers
        self.df_CVRs["avgBounceRate"] = self.df_CVRs.bounces / self.df_CVRs.sessions

        for col in self.cols_to_analyze:
            self.df_CVRs["CVR_{}".format(col)] = self.df_CVRs[col] / self.df_CVRs.uniqueUsers

        # variants
        variants = self.gen_variants_dict(self.df_CVRs.experimentVariant)
        self.df_CVRs["experimentVariant"] = self.df_CVRs["experimentVariant"].map(int).map(variants)

        self.df_CVRs = self.df_CVRs.groupby(group_by_cols).sum().reset_index()

    @staticmethod
    def Z_test(Z_score):
        abs_Z_score = abs(Z_score)
        return 1 - scipy.special.ndtr(abs_Z_score)


    # As input had DataFame with calculated CVR and list of columns to analyse, used to calculate: Change_in_Conversion, Z-score, P-value, 90% significance, 95% significance
    def calculate_statistic(self, control: str = "Control") -> pd.DataFrame:
        # Divide part with and without control
        df = self.df_CVRs
        df_control = df[df.experimentVariant == control]
        df_without_control = df[df.experimentVariant != control]

        # Calculate all needed data
        for col in self.cols_to_analyze:
            df_without_control["Change_in_Conversion_{}".format(col)] = df_without_control["CVR_{}".format(col)] / \
                                                                        df_control["CVR_{}".format(col)].iloc[0] - 1

            # TODO: rewrite, introduce local varaibles so we know what the formula is, now it is unclear
            df_without_control["Z-score_{}".format(col)] = (df_control["CVR_{}".format(col)].iloc[0] - df_without_control[
                "CVR_{}".format(col)]) / ((df_without_control["SE_{}".format(col)] ** 2 +
                                           df_control["SE_{}".format(col)].iloc[0] ** 2).pow(1. / 2))

            Z_score = df_without_control["Z-score_{}".format(col)]
            df_without_control["p-value_{}".format(col)] = self.Z_test(Z_score)

            p_value = df_without_control["p-value_{}".format(col)]
            df_without_control["90% significance_{}".format(col)] = p_value.apply(Analysis.significance90)
            df_without_control["95% significance_{}".format(col)] = p_value.apply(Analysis.significance95)

        return pd.concat([df_control, df_without_control], ignore_index=True, sort=False)


    # Calculate all at one place, main function to run. A input had dataframe, list columns to group by (variants and devices) and columns to analyze
    def analyze_test(self) -> List[pd.DataFrame]:
        significant_difference = []
        not_significant_difference = []

        for group in self.group_by_cols:
            print(group)
            self.generate_cvrs(group)
            for col in self.cols_to_analyze:
                self.df_CVRs["SE_{}".format(col)] = (
                            self.df_CVRs["CVR_{}".format(col)] * (1 - self.df_CVRs["CVR_{}".format(col)]) / self.df_CVRs[
                        'uniqueUsers']).pow(1. / 2)

            if len(group) == 1:
                analysis_type = "variants"
                self.analysis_types.append(analysis_type)
                entire_df = self.calculate_statistic()
                for current_col in self.cols_to_analyze:
                    columns_to_include = ["experimentVariant", "uniqueUsers"] + [col for col in entire_df.columns if
                                                                                 current_col in col]
                    df_column = entire_df[columns_to_include]
                    significant_90 = df_column.iloc[:, -2]
                    if significant_90.any() == 'Yes':
                        difference = "significant difference"
                        significant_difference.append((col, df_column))
                        self.result_difference[(analysis_type, difference)] = significant_difference
                    else:
                        difference = "no difference among variants"
                        not_significant_difference.append((col, df_column))
                        self.result_difference[(analysis_type, difference)] = not_significant_difference
                    self.result[(analysis_type, current_col)] = df_column
            else:
                analysis_type = "main_analysis"
                self.analysis_types.append(analysis_type)
                device_types = self.df_CVRs.deviceType.unique()
                self.device_types = list(device_types)
                # experiment_variants=[variant for variant in df_with_cvrs.experimentVariant.unique() if variant != control]
                # return {(device, cols_to_analyze): calculate_statistic(df_with_cvrs[df_with_cvrs.deviceType==device], cols_to_analyze) for device in device_types}
                # TODO: to decide what should it be a list, or dict and what should be the key

                for device in device_types:

                    entire_df = self.calculate_statistic()
                    for current_col in self.cols_to_analyze:

                        columns_to_include = ["experimentVariant", "deviceType", "uniqueUsers"] + [col for col in
                                                                                                   entire_df.columns if
                                                                                                   current_col in col]
                        df_column = entire_df[columns_to_include]
                        significant_90 = df_column.iloc[:, -2]
                        if significant_90.any() == 'Yes':
                            difference = "significant difference"
                            significant_difference.append((col, df_column))
                            self.result_difference[(analysis_type, difference)] = significant_difference
                        else:
                            difference = "no difference among variants"
                            not_significant_difference.append((col, df_column))
                            self.result_difference[(analysis_type, difference)] = not_significant_difference

                        self.result[(analysis_type, device, current_col)] = df_column
        self.all_difference = ['significant difference', "no difference among variants"]
        # return {device: calculate_statistic(df_with_cvrs[df_with_cvrs.deviceType==device], cols_to_analyze) for device in device_types}
