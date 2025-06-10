
import statsmodels.api as sm
from ISLP.models import ModelSpec as MS
import pandas as pd
import numpy as np

def linear_regresion_per_state(data, y_input:str, X_input:list): 

    # 1. Filter for one state 
    # 2. Arrange by date 
    # 3. Calc temp - temp(t=-365)
    # Calc first oder difference in revenue
    # for each state filter out days which were only used to calc temp-365 / meaning the day bevore revenue was recorded

    results_df = pd.DataFrame(columns=["State", "R^2", "R^2 Adj", "coefficient_variables"])
    states_list = data["Shipping Address State"].unique()

    for state in states_list: 
        state_filter = data["Shipping Address State"] == state
        df_one_state = data[state_filter].copy()

        df_one_state = df_one_state.sort_values("Order Date", ascending=True)

        # Temp no season 
        df_one_state["Temp_No_Season"] = df_one_state["tavg"] - df_one_state["tavg"].shift(365)
        df_one_state["Temp_No_Season"] = df_one_state["Temp_No_Season"].round(3)

        # Rain no season
        df_one_state["Rain_No_Season"] = df_one_state["ppt"] - df_one_state["ppt"].shift(365)
        df_one_state["Rain_No_Season"] = df_one_state["Rain_No_Season"].round(3)

        # First order diff of Revenue 
        first_order_diff = [0]

        for j in range(1,len(df_one_state)): 
            first_order_diff.append(df_one_state["Revenue"].iloc[j] - df_one_state["Revenue"].iloc[j-1])

        df_one_state["first_order_diff_Revenue"] = first_order_diff
        df_one_state["first_order_diff_Revenue"] = df_one_state["first_order_diff_Revenue"].round(4)

        # Lag first order diff of Revenue by 1 day
        df_one_state.loc[:, "first_order_diff_Revenue_lagged"] = df_one_state["first_order_diff_Revenue"].shift(-1)

        # Calc SMA7 for Hot, Cold, Rain Clothing
        df_one_state.loc[:, "SMA7_ratio_hot_weather_clothing"] = df_one_state["ratio_hot_weather"].rolling(7).mean().round(2)

        df_one_state.loc[:, "SMA7_ratio_cold_weather_clothing"] = df_one_state["ratio_cold_weather"].rolling(7).mean().round(2)

        df_one_state.loc[:, "SMA7_ratio_rain_weather_clothing"] = df_one_state["ratio_rain_protection"].rolling(7).mean().round(2)

        # Remove days bevore revenue was collected 
        df_one_state = df_one_state.iloc[365:, :]

        # Adding a linear count column -> should represent later entries in the regression
        df_one_state.loc[:, 'Time'] = np.arange(len(df_one_state))

        # Fill NA with 0
        df_one_state = df_one_state.fillna(0)

#################### Linear Regression #########################
        X = MS(X_input).fit_transform(df_one_state)
        y = df_one_state[y_input]


        model = sm.OLS(y, X)
        results = model.fit()

        """coef_dict = {
            name: {
                'coefficient': coef,
                'p_value': pval
            }
            for name, coef, pval in zip(results.model.exog_names, results.params.round(3), results.pvalues.round(3))
        }

        new_row = {"State":state, "R^2": results.rsquared.round(3), "R^2 Adj": results.rsquared_adj.round(3), "coefficient_variables": coef_dict}
        #print(regression)
        results_df.loc[len(results_df)] = new_row """

        # Create the base data
        base_data = {
            ("Info", "State"): state,
            ("Model Fit", "R^2"): results.rsquared.round(3),
            ("Model Fit", "R^2 Adj"): results.rsquared_adj.round(3)
        }

        # Add coefficient data
        for name in results.model.exog_names:
            base_data[("Coefficients", name)] = results.params[name].round(3)
            base_data[("P-values", name)] = results.pvalues[name].round(3)

        # Create MultiIndex columns
        columns = pd.MultiIndex.from_tuples(list(base_data.keys()))

        # Create a new row as a DataFrame with MultiIndex columns
        new_row = pd.DataFrame([base_data], columns=columns)

        # If this is the first row, create the DataFrame with MultiIndex columns
        if len(results_df) == 0:
            results_df = new_row
        else:
            # Make sure both DataFrames have the same column structure
            results_df = pd.concat([results_df, new_row], ignore_index=True)

    return results_df
    




######################### Example execution ################################
# fashion_df = pd.read_csv("./data/fashion_data.csv")
# fashion_df["Order Date"] = pd.to_datetime(fashion_df["Order Date"]) # Formating Order date back to Datetime dtype, in read_csv you cant set column to datetime so need to do manually
# fashion_df.set_index("Order Date", inplace=True)
# fashion_df.drop(columns=["Unnamed: 0"], inplace=True)

# fashion_df = fashion_df.fillna(0)


# Lin_reg_Rev_Big_cold_weather_clo= linear_regresion_per_state(fashion_df, y_input="SMA7_ratio_cold_weather_clothing", X_input=["Temp_No_Season", "Rain_No_Season", "first_order_diff_Revenue_lagged", "tavg", "ppt", "Time"])



#print(regression)