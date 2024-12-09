# TBD's 11.12
1. Currently, we do not have temperature information for the states of Alaska, Hawaii, Puerto Rico, District of Columbia 

-> In the current code, I simply removed them

2. I used simple moving averages for 7,14,30 days when working with the revenue values in the Granger test 

-> What is your opinion/is there something I should consider

3. Correct for growth trend in Revenue:
In the current version of the Grabger Causation Test, only a small number of (around 13 states with SMA30) states have a significant effect on Revenue caused by temperature (lag is set to 12). From my information, the underlying cause is a growing revenue trend across the majority of states caused by an increase in customers in our data set. 

-> Thesis: We need to correct the Revenue for the growth trend to get an accurate Granger Causation. 