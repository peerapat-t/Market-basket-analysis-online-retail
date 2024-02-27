# %%
import warnings
warnings.simplefilter("ignore")

# %%
import streamlit as st

# %%
import pandas as pd

# %%
import json

# %%
import ast

# %% [markdown]
# # Import trained model

# %%
final_result_df = pd.read_excel('final_result.xlsx')

# %%
final_result_df = final_result_df[['antecedents','consequents','confidence']]

# %%
final_item_df = pd.read_excel('item_name_final.xlsx')

# %%
item_list = sorted(final_item_df['Description'].unique().tolist())

# %% [markdown]
# # Prediction function

# %%
def recommendation_prediction(buy_item_list, final_result_df):
    recommendation_list = []
    for index, row in final_result_df.iterrows():
        if sorted(set(buy_item_list)) == sorted(set(ast.literal_eval(row['antecedents']))):
            antecedents = sorted(set(ast.literal_eval(row['antecedents'])))
            consequents = sorted(ast.literal_eval(row['consequents']))
            confidence = row['confidence']
            recommendation_list.append([antecedents, consequents, confidence])

    df = pd.DataFrame(columns=['antecedents', 'consequents', 'count_consequents', 'confidence'])
    
    for data in recommendation_list:
        df = pd.concat([df, pd.DataFrame({
            'antecedents': [data[0]],
            'consequents': [data[1]],
            'count_consequents': len(data[1]),
            'confidence': data[2]
            })], ignore_index=True)
        
    df = df.sort_values(by=['confidence', 'count_consequents'], ascending=[False, True])

    return df

# %% [markdown]
# # Prediction function

# %%
def main():
    st.title('Online retail selling signal')

    item_option1 = st.selectbox("Item number 1:", item_list, key='item_option1')
    item_option2 = st.selectbox("Item number 2:", item_list, key='item_option2')
    item_option3 = st.selectbox("Item number 3:", item_list, key='item_option3')
    item_option4 = st.selectbox("Item number 4:", item_list, key='item_option4')
    item_option5 = st.selectbox("Item number 5:", item_list, key='item_option5')

    input_list = [item_option1, item_option2, item_option3, item_option4, item_option5]
    input_list = [x for x in input_list if x != 'No item']
    input_list = list(set(input_list))

    output = ''
    prediction_result_df = []

    if st.button('Predict'):
        prediction_result_df = recommendation_prediction(input_list)
        st.dataframe(prediction_result_df)

# %%
if __name__ == '__main__':
    main()


