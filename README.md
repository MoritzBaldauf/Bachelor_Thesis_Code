# TBD's 11.12
1. Currently, we do not have temperature information for the states of Alaska, Hawaii, Puerto Rico, District of Columbia 

-> In the current code, I simply removed them

2. I used simple moving averages for 7,14,30 days when working with the revenue values in the Granger Test 

-> What is your opinion/is there something I should consider

3. Correct for growth trend in Revenue:
In the current version of the Granger Test, only a small number of (around 13 with SMA30) states show a significant effect of temperature on revenue (lag is set to 12). From my information, this is caused by an underlying growth in revenue across the majority of states caused by an increase in customers in our data set. 

-> Thesis: We need to correct the Revenue for the growth trend to get an accurate Granger Causation. 
