import matplotlib
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
import json
import pandas as pd
import os
import ast
from dotenv import load_dotenv
load_dotenv()

class DataProcessor:
    def __init__(self, file):
        self.file = file
        file_path = f"csv_{file}"
        url = os.environ.get(file_path)
        self.df = self.load_data(url)
        
    def load_data(self, file_path):
        data = pd.read_csv(file_path)
        return data
    
    # @staticmethod
    def remove_last_part(s):
        last_index = s.rfind('_')
        return s[:last_index] if last_index != -1 else s
    
    def get_model_names(self):
        if self.file == 2023:
            models = {
                "gpt_full_result": "Model GPT4 + Full Content + one-shot",
                "gpt_selected_result": "Model GPT4 + Selected Content + one-shot",
                "gpt_summary_result": "Model GPT4 + Summary + one-shot",
                "claude_selected_result":"Model Claude + Selected Content + one-shot",
                "claude_criteria_result":"Model Claude + Selected Content + criterion per shot",
            }
        elif self.file == 2024:
            models = {
                "hd_result": "Model HD + Full Content + one-shot (Charles/Justin)",
                "gpt_result": "Model GPT4 + Full Content + one-shot (AI Sprouts)",
                "claude_result": "Model Claude + Selected Content + one-shot (AI Sprouts)",
            } 
        model_key = models.keys()
        self.model_names = [DataProcessor.remove_last_part(model) for model in model_key]
        print(self.model_names)
        return self.model_names

    def print_metrics(self, model):
        self.confusion_matrix = pd.crosstab(self.df['Advance'], 
                                       self.df[f'{model}_advance'], 
                                       rownames=['Actual'], 
                                       colnames=[model], 
                                       margins=True)
        print(self.confusion_matrix, "\n")

        TP = self.confusion_matrix.loc[True, True]  # True Positives
        TN = self.confusion_matrix.loc[False, False]  # True Negatives
        FP = self.confusion_matrix.loc[False, True]  # False Positives
        FN = self.confusion_matrix.loc[True, False]  # False Negatives

        accuracy = (TP + TN) / self.confusion_matrix.loc['All', 'All']
        precision = TP / (TP + FP) if (TP + FP) != 0 else 0
        recall = TP / (TP + FN) if (TP + FN) != 0 else 0
        f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) != 0 else 0

        if model == 'gpt':
            model_name = 'gpt-4-0125-preview'
        elif model == 'claude':
            model_name = 'claude-3-opus-20240229'
        else:
            model_name = model
        print(f"Model: {model_name}")
        print(f"Accuracy: {accuracy:.4f}")
        print(f"Precision: {precision:.4f}")
        print(f"Recall: {recall:.4f}")
        print(f"F1-Score: {f1_score:.4f} \n" )

        self.metrics = {
            "model": model_name,
            "accuracy": f"{accuracy:.4f}",
            "precision": f"{precision:4f}",
            "recall": f"{recall:.4f}",
            "f1_score": f"{f1_score:4f}"
        }
        return self.confusion_matrix, self.metrics

    def get_metrics(self):
        self.model_metrics = []
        self.conf_matrices = []
        for model in self.model_names:
            print(model)
            cm, m = DataProcessor.print_metrics(self, model)
            self.model_metrics.append(m)
            self.conf_matrices.append(cm)
            print(self.model_metrics, self.conf_matrices)
        return self.model_metrics, self.conf_matrices

class Plotter:
    def __init__(self, data_processor):
        self.data_processor = data_processor
        self.df = data_processor.df
        self.model_names = data_processor.get_model_names()


    def plot_confusion_matrix(self):
        self.model_metrics, self.conf_matrices = self.data_processor.get_metrics()
        fig, axes = plt.subplots(nrows=1, ncols=5, figsize=(12, 5))

        for i, model in enumerate(self.model_names):
            actual_false, actual_true = self.conf_matrices[i][False][:2], self.conf_matrices[i][True][:2]
            bar_width = 0.35
            index = np.arange(2)
            
            axes[i].bar(index, actual_false, bar_width, label='Predicted False')
            axes[i].bar(index, actual_true, bar_width, bottom=actual_false, label='Predicted True')
            
            axes[i].set_title(f'{model.replace("_", " ").title()}')
            axes[i].set_xticks(index)
            axes[i].set_xticklabels(['False', 'True'])
            # axes[i].set_xlabel('Actual')
            axes[i].set_ylabel('Count')
            # axes[i].legend()

        # Set the legend for the whole figure, outside the loop
        fig.legend(['Predicted False', 'Predicted True'], loc='upper right', ncol=2)
        fig.suptitle('Confusion Matrix', fontsize=16)
        # Adding a common xlabel using fig.text
        fig.text(0.5, 0.04, 'Actual', ha='center', va='center', fontsize=12)

        plt.tight_layout(rect=[0, 0.03, 1, 0.95])
        plt.show()

    def plot_metrics(self):
        self.model_metrics, self.conf_matrices = self.data_processor.get_metrics()
        df = pd.DataFrame(self.model_metrics)
        df = df.drop(2, axis=0)
        df['accuracy'] = df['accuracy'].astype(float)
        df['precision'] = df['precision'].astype(float)
        df['recall'] = df['recall'].astype(float)
        df['f1_score'] = df['f1_score'].astype(float)

        # Set index to model for better plotting
        df.set_index('model', inplace=True)
        palette = plt.get_cmap('Set1')
        # Plotting
        fig, axes = plt.subplots(1, 4, figsize=(12, 5))  # Subplots for each metric
        metrics = ['accuracy', 'precision', 'recall', 'f1_score']
        for ax, metric in zip(axes.flatten(), metrics):
            for i, (index, row) in enumerate(df.iterrows()):
                ax.bar(index, row[metric], color=palette(i), label=f"{index}" if metric == 'accuracy' else "")
            ax.set_title(metric.capitalize())
            ax.set_ylabel('Score')
            ax.set_xticks([]) 
            # ax.set_xticklabels(df.index, rotation=45, ha='right')

        # Add the legend to the figure, not to the subplot
        handles, labels = axes[0].get_legend_handles_labels()
        fig.legend(handles, labels, loc='lower center', ncol=len(df.index), frameon=False)

        fig.suptitle('Model Performance Metrics', fontsize=16)
        plt.tight_layout(rect=[0, 0.03, 1, 0.95])
        plt.show()

    def check_fail_criteria(self, message):
        failreason = []
        for i in range(1, 5):
            criteria = message[f'criterion_{i}']
            if criteria['result'] == 'fail':
                failreason.append(i)
        fail_str = ', '.join(map(str, failreason)) 
        return fail_str

    def count_false(self):
        df_count = {
            'GPT4 critierion per shot': self.df['hd_advance'].value_counts(),
            'Claude3 selected columns': self.df['claude_selected_advance'].value_counts(),
            'GPT4 selected columns': self.df['gpt_selected_advance'].value_counts()
        }
        df_count = pd.DataFrame(df_count)
        return df_count
    

    def difference_decision(self):
        diff_df = self.df.loc[(self.df['hd_advance'] != self.df['claude_selected_advance']) | (self.df['hd_advance'] != self.df['gpt_selected_advance']),['Solution ID','hd_advance','hd_failreason','claude_selected_advance', 'claude_selected_result', 'gpt_selected_advance', 'gpt_selected_result']]
        print(diff_df)
        return diff_df

    def print_diff_decision(self):
        diff = self.difference_decision()
        diff['gpt_selected_failreason'] = diff.apply(lambda x: self.check_fail_criteria(ast.literal_eval(x['gpt_selected_result'])), axis=1)
        diff['claude_selected_failreason'] = diff.apply(lambda x: self.check_fail_criteria(ast.literal_eval(x['claude_selected_result'])), axis=1)
        diff.drop(columns=['gpt_selected_result', 'claude_selected_result'], inplace=True)
        diff.rename(columns={'hd_failreason': 'GPT4 critierion per shot Fail Reason',
                            'hd_advance': 'GPT4 critierion per shot',
                            'claude_selected_advance': 'Claude3 selected columns',
                            'claude_selected_failreason': 'Claude3 critierion per shot Fail Reason',
                            'gpt_selected_advance': 'GPT4 selected columns',
                            'gpt_selected_failreason': 'GPT4 selected columns Fail Reason'}, inplace=True)
        # print(diff)
        return diff

def main(file:int):
    if not isinstance(file, int):
        raise TypeError("Expected an integer for 'file'")
    if file == 2023:
        file_path = os.environ.get('csv_2023')
        processor = DataProcessor(file_path)
        model_names = processor.get_model_names()
        model_metrics, conf_matrices = processor.get_metrics()
        plotter = Plotter(processor)
        plotter.plot_metrics()
        plotter.plot_confusion_matrix()
    elif file == 2024:
        file_path = os.environ.get('csv_2024')
        processor = DataProcessor(file_path)
        model_names = processor.get_model_names()
        plotter = Plotter(processor)
        plotter.count_false()
        plotter.print_diff_decision()


if __name__ == '__main__':
    main(file=2024)
