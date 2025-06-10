import statsmodels.api as sm
import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import grangercausalitytests




def Granger_Causality_test_per_state(df, states, log, sma, lag = 12, test = "ssr_chi2test", rolling_value = 7): 
    results = pd.DataFrame(columns=['State', 'Sales_Tavg', 'Datapoints'])


    def grangers_causation_matrix(data, variables, maxlag= lag, test=test, verbose=False):    
                df = pd.DataFrame(np.zeros((len(variables), len(variables))), columns=variables, index=variables)
                for c in df.columns:
                    for r in df.index:
                        test_result = grangercausalitytests(data[[r, c]], maxlag=maxlag, verbose=False)
                        p_values = [round(test_result[i+1][0][test][1],4) for i in range(maxlag)]
                        if verbose: print(f'Y = {r}, X = {c}, P Values = {p_values}')
                        min_p_value = np.min(p_values)
                        df.loc[r, c] = min_p_value
                df.columns = [var + '_x' for var in variables]
                df.index = [var + '_y' for var in variables]
                return df

    
    
    for state in states:
        try:
            state_filter = df["Shipping Address State"] == state # Create subset for only one state
            df_one_state_filtered = df[state_filter]

            df_granger_test = df_one_state_filtered.groupby("Order Date").agg({"Revenue": "sum", "tavg":"first"})
            
            #df_granger_test = df_one_state[["Revenue", "tavg"]] 
            if sma: 
                df_granger_test["Revenue"] = df_granger_test["Revenue"].rolling(rolling_value).mean()

                df_granger_test = df_granger_test.iloc[rolling_value-1:] # removing the missing values resulting from SMA
            
            result_one_state = grangers_causation_matrix(df_granger_test, variables = df_granger_test.columns) 

            
            new_row = {"State":state, "Sales_Tavg": result_one_state["tavg_x"][0], "Datapoints": len(df_one_state_filtered)}
            if log:
                print(state)

            results.loc[len(results)] = new_row 
        except ValueError: # Error handling for missing values for a single state 

            new_row = {"State":state, "Sales_Tavg": "NaN", "Datapoints": len(df_one_state_filtered)} # Add empty entry 
            results.loc[len(results)] = new_row 
            print(f"State with ValueError:{state}")
            continue

    return results 

# Test execution
#Granger_matrix_fashion_14 = Granger_Causality_test_per_state(df_granger_test, states_list, sma=True, log= False,rolling_value=30)