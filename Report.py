# title Select the AB test report to display
import ipywidgets as widgets
from IPython.core.display import HTML, display


class Report:

    def __init__(self, Analysis):
        self.Analysis = Analysis
        self.output = widgets.Output()
        self.dropdown_analysis_type = widgets.Dropdown(options=Analysis.analysis_types, description="Analysis type: ")
        self.dropdown_device = widgets.Dropdown(options=Analysis.device_types, description="Device type: ")
        self.dropdown_column = widgets.Dropdown(options=Analysis.cols_to_analyze, description="Column: ")

        self.button = widgets.Button(description="Show report")
        self.button_all = widgets.Button(description="Show all")

        display(self.dropdown_analysis_type, self.dropdown_device, self.dropdown_column,
                     self.button, self.button_all, self.output)

    @staticmethod
    def table_has_significant_results(df):
        p_val = df.iloc[:, -2]

        if p_val.any() == "Yes":
            return "<font color='red'>significant difference</font>"
        else:
            return "<font color='green'>no difference among variants</font>"

    def show_all(self, b):
        with self.output:
            self.output.clear_output()

            for key in self.Analysis.result.keys():
                try:
                    df = self.Analysis.result[key]
                    if 'deviceType' in df:
                        df = df.drop(["deviceType"], axis=1)

                    df.columns = [col.replace('_' + key[1], '') for col in df.columns]
                    display(HTML("<h1>" + key[0] + ", " + key[1] + ", " + self.table_has_significant_results(df) + "</h1>"))
                    df = df.fillna('')
                    display(df)
                except Exception:
                    print(f'No such values: {key}')

    def on_button_clicked(self, b):
        with self.output:
            self.output.clear_output()
            try:
                if self.dropdown_analysis_type.value == "variants":
                    df = self.Analysis.result[(self.dropdown_analysis_type.value, self.dropdown_column.value)]
                else:
                    df = self.Analysis.result[(self.dropdown_analysis_type.value, self.dropdown_device.value, self.dropdown_column.value)]
                    df = df.drop(["deviceType"], axis=1)
                if type(df) != list:
                    df.columns = [col.replace('_' + self.dropdown_column.value, '') for col in df.columns]
                display(HTML(
                    "<h1>" + self.dropdown_analysis_type.value + ",  " + self.dropdown_column.value + ", "
                    + self.dropdown_device.value + ", " + self.table_has_significant_results(
                        df) + "</h1>"))
                df = df.fillna('')
                display(df)
                display(HTML("<br/><br/>"))
            except Exception:
                print(f'No such values: {self.dropdown_analysis_type.value}, {self.dropdown_difference.value}')

    def button_actions(self):
        self.button.on_click(self.on_button_clicked)
        self.button_all.on_click(self.show_all)