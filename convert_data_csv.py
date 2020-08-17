from process.data_generation import convert_data_to_csv
import pandas as pd

if __name__ == "__main__":
    convert_data_to_csv('data/images/', 'data/labels/')
    class_list_df = pd.DataFrame({'class_name': ['vertical'], 'id': [0]})
    class_list_df.to_csv('class_list.csv')
