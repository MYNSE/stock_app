All endpoints use POST requests with JSON data

### [POST] /v1/add_stock

Adds a stock to the portfolio. Downloads data from Yahoo Finance
if required.

Required:
 - ticker: the yahoo finance ticker of the stock to add

### [POST] /v1/add_fixed_rate

Adds a fixed rate asset, with a fixed interest rate
and period, to the portfolio.

Required: 
 - symbol: the symbol to use for the asset. Asset symbol will be prepended with
'fixed_' if it is not already.

Optional: 
 - rate: the annual interest rate of the asset. Currently, we assume that the interest rate will compound monthly

### [POST] /v1/get_user_data

Returns user data as a JSON

### [POST] /v1/remove_symbol

Removes a symbol

Required:
 - symbol: the one to remove