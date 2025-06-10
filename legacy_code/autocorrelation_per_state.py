import pandas as pd

# Take df of 
#1 subset 
#2 order 
#3 first order diff 
#4 Autocorrelation 


def autocorrelation_per_state(data): 
    states_list = data["Shipping Address State"].unique()
    results_df = pd.DataFrame(columns=['State', 't', 't+1','t+2','t+3','t+4','t+10','t+14'])

    for state in states_list: 
        # Filter for only one State
        state_filter = data["Shipping Address State"] == state # Create subset for only one state
        df_one_state = data[state_filter]

        # Order datapoints by date 
        df_one_state = df_one_state.sort_values("Order Date", ascending=True)

        # Calculate first order diff
        first_order_diff = [0]
        for j in range(1,len(df_one_state)): 
            first_order_diff.append(df_one_state["Revenue"][j] - df_one_state["Revenue"][j-1])
        
        df_one_state["first_order_diff_Revenue"] = first_order_diff

        # Calculate autocorrelation
        series = df_one_state["first_order_diff_Revenue"]

        # using shift function to shift the values.
        dataframe = pd.concat([series.shift(14), series.shift(10), series.shift(4), series.shift(3), series.shift(2), series.shift(1), series], axis=1)
        # naming the columns
        dataframe.columns = ['t', 't+1', 't+2', 't+3', 't+4', 't+10', 't+14']

        # using corr() function to compute the correlation
        result = dataframe.corr()
        new_row = {"State": state, "t": result.iloc[0,0], "t+1": result.iloc[0,1], "t+2": result.iloc[0,2], "t+3": result.iloc[0,3], "t+4": result.iloc[0,4], "t+10": result.iloc[0,5], "t+14": result.iloc[0,6]}
        results_df.loc[len(results_df)] = new_row

    return results_df