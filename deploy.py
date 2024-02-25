# %%
import streamlit as st

# %%
import pandas as pd

# %%
import json

# %% [markdown]
# # Import trained model

# %%
# Loading JSON data from file
with open("output.json", "r") as json_file:
    recommendation_rule = json.load(json_file)

# %% [markdown]
# # Create function

# %%
def recommendation_prediction(buy_item_set):
    recommendation_list = []
    for rule in recommendation_rule:
        if set(buy_item_set).issubset(set(rule['origin'])):
            recommendation_list.append([rule['origin'], rule['destination'], rule['confidence']])
    
    df = pd.DataFrame(columns=['origin', 'destination', 'count_destination', 'confidence'])
    for data in recommendation_list:
        df = pd.concat([df, pd.DataFrame({
            'origin': [data[0][0]],
            'destination': [', '.join(data[1][0].split(', '))],
            'count_destination': [len(data[1][0].split(', '))],
            'confidence': [data[2]]
            })], ignore_index=True)

    df['count_destination'] = pd.to_numeric(df['count_destination'], errors='coerce')
    df = df.groupby(['origin', 'destination']).apply(lambda x: x.nlargest(1, 'confidence').nsmallest(1, 'count_destination')).reset_index(drop=True)

    # If still multiple rows exist, randomly select one
    if len(df) > 1:
        df = df.sample(n=1)
    return df

# %% [markdown]
# # Prediction function

# %%
def main():
    st.title('Car insurance selling signal')

    itm_list = ['No item',
                '60 TEATIME FAIRY CAKE CASES',
                '72 SWEETHEART FAIRY CAKE CASES',
                '60 TEATIME FAIRY CAKE CASES',
                'PACK OF 60 PINK PAISLEY CAKE CASES',
                'CHOCOLATE HOT WATER BOTTLE',
                'HOT WATER BOTTLE TEA AND SYMPATHY',
                'HOME BUILDING BLOCK WORD',
                'LOVE BUILDING BLOCK WORD',
                'STRAWBERRY CERAMIC TRINKET BOX',
                'SWEETHEART CERAMIC TRINKET BOX',
                'VINTAGE HEADS AND TAILS CARD GAME',
                'VINTAGE SNAP CARDS',]

    item_option1 = st.selectbox("Item number 1:", itm_list, key='item_option1')
    item_option2 = st.selectbox("Item number 2:", itm_list, key='item_option2')
    item_option3 = st.selectbox("Item number 3:", itm_list, key='item_option3')
    item_option4 = st.selectbox("Item number 4:", itm_list, key='item_option4')
    item_option5 = st.selectbox("Item number 5:", itm_list, key='item_option5')

    input_list = [item_option1, item_option2, item_option3, item_option4, item_option5]
    input_list = [x for x in input_list if x != 'No item']

    output = ''
    if st.button('Predict'):
        prediction_result_df = recommendation_prediction(input_list)

        if prediction_result_df.shape[0] == 0:
            output = 'No recommendation'
        else:
            output = recommendation_prediction(['STRAWBERRY CERAMIC TRINKET BOX'])['destination'][0]

    st.success(f'Prediction Result: {output}')

# %%
if __name__ == '__main__':
    main()


