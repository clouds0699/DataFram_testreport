import pandas as pd
from jinja2 import Environment, FileSystemLoader

# 创建示例数据
data_result = {'id': ["twqewqewq1", "twqewq2", "ewqewq3", "twqeqw4"],
               'column1': ['Aaaddsadsa', 'B', 'C', 'D'],
               'column2': ['A', 'B', 'C', 'D'],
               'column3': ['A', 'B', 'C', 'D'],
               'column4': ['A', 'B', 'C', 'D'],
               'column5': ['A', 'B', 'C', 'D'],
               'column6': ['Aasdqwewqewqeqwe', 'B', 'C', 'D'],
               'column7': [10, 20, 30, 40]}
df_result = pd.DataFrame(data_result)

data_expected = {'id': ["twqewqewq1", "twqewq2", "ewqewq3", "twqeqw4"],
                 'column1': ['BdsadsadsadBdsadsadsadBdsadsadsa', 'D', 'D', 'D'],
                 'column2': ['Rdsadsadsa', 'B', 'C', 'D'],
                 'column3': ['A', 'D', 'D', 'D'],
                 'column4': ['RdsadsadRdsadsadRdsadsadRdsadsadRdsadsad', 'B', 'C', 'D'],
                 'column5': ['B', 'D', 'D', 'D'],
                 'column6': ['R', 'B', 'C', 'D'],
                 'column7': [20, 25, 30, 20]}
df_expected = pd.DataFrame(data_expected)

# 根据'id'列进行合并
merged_df = pd.merge(df_result, df_expected, on='id', suffixes=('_result', '_expected'))

# 判断两个DataFrame中对应行的列是否相同，并添加相应的列
merged_df['is_match'] = merged_df.drop('id', axis=1).apply(
    lambda row: row['column1_result'] == row['column1_expected'] and row['column2_result'] == row['column2_expected'],
    axis=1)

# 筛选出匹配上的数据中其余列不相同的行
mismatched_rows = merged_df[merged_df['is_match'] == False].drop('is_match', axis=1)

# 创建一个空列表来存储所有的行
all_data = []
# 遍历合并后的DataFrame
for index, row in mismatched_rows.iterrows():
    # 创建一个空字典来存储所有的列
    all_columns = {}
    # 遍历每一列，跳过'id'列
    for column in df_result.columns.drop('id').tolist():
        # 将结果和预期值添加到字典中
        all_columns[column] = (row[column + '_result'], row[column + '_expected'])
    # 将id和所有的列添加到列表中
    all_data.append({'id': row['id'], 'columns': all_columns})

# 使用列表创建一个新的DataFrame
all_df = pd.DataFrame(all_data)

# 统计结果
total_rows_result = len(df_result)
total_rows_expected = len(df_expected)
matched_rows = merged_df.shape[0]
matched_rows_same = merged_df[(merged_df['is_match'])].shape[0]
matched_rows_diff = len(mismatched_rows)
all_columns = df_result.columns.drop('id').tolist()

# 渲染测试报告模板
env = Environment(loader=FileSystemLoader('templates'))
template = env.get_template('report_template.html')  # 假设模板文件为report_template.html

# 渲染模板并生成测试报告
report = template.render(total_rows_result=total_rows_result,
                         total_rows_expected=total_rows_expected,
                         matched_rows=matched_rows,
                         matched_rows_same=matched_rows_same,
                         matched_rows_diff=matched_rows_diff,
                         all_df=all_df,
                         all_columns=all_columns)

# 将测试报告写入文件
with open('test_report.html', 'w', encoding='utf-8') as f:
    f.write(report)
