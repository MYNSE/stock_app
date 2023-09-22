# Adding assets

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