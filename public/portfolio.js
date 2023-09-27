// ENDPOINTS
const baseURL = window.location.href //ends with /
const addStockEndpoint = baseURL + 'v1/add_stock'
const removeSymbolEndpoint = baseURL + 'v1/remove_symbol'
const userDataEndpoint = baseURL + 'v1/get_user_data'

const addNewAssetForm = document.getElementById('variable-form')
const symbolsList = document.getElementById('symbols-list')

let assetFormState = 'empty';
const addStockForm = 
`<div id="add-asset-form">
<div class="sb-form-field">
    <p>Ticker: </p>
    <input type="text" placeholder="e.g. AAPL" id="stock-ticker" autocomplete="off">
</div>
<div class="sb-form-field">
    <button class="sidebar-button" onclick="addStock()">go</button>
</div>
</div>`

// RENDER THE PAGE
renderPage()

// FUNCTIONS FOR RENDERING THE PAGE
async function renderPage() {
    const userData = await getUserDataFromEndpoint()
    renderStocksInPortfolio(userData)
}

async function getUserDataFromEndpoint() {
    /*
    Gets ALL user data from API endpoint
    */
    const response = await fetch(userDataEndpoint, {
        method: 'POST'
    })

    const data = await response.json()
    return data
}

function renderStocksInPortfolio(userDataJson) {
    /*
    Renders stocks in portfolio based on user data returned from
    API endpoint.
    */
    let stocks = userDataJson.portfolio.symbols
    let htmlString = ''
    let symbol = ''
    for (let i=0; i < stocks.length; i++) {
        symbol = stocks[i]
        htmlString +=
        `
        <div class="symbol-info sidebar-text sidebar-text-hover">
            <p class="symbol">${symbol}</p>
            <div class="ticker-buttons">
                <button onclick="removeSymbolButtonOnclick(this)">Remove</button>
            </div>
        </div>
        `
    }
    symbolsList.innerHTML = htmlString
}

// FUNCTIONS FOR THE 'ADD ASSET' FORMS
function renderAddAssetForm(mode, content) {
    /*
    Renders the "add asset" form.
    
    A different form will open if you press the three buttons
    If you press the same button again, the form will close.
    If you press a different button, the new form will pop up.
    */
    if (assetFormState == mode) {
        addNewAssetForm.innerHTML = ''
        assetFormState = 'empty'
    } else {
        addNewAssetForm.innerHTML = content
        assetFormState = mode
    }
}

function addAssetFormAlert(alert) {
    /*
    Adds an alert where the asset form should go,
    indicating an operation failed.
    */
    addNewAssetForm.innerHTML = `
    <div class="gd-container sidebar-text">
        <p class="alert">${alert}</p>
    </div>`
    assetFormState = 'empty'
}

// FUNCTIONS FOR ADDING/REMOVING STOCKS
function addStockButtonOnclick() {
    renderAddAssetForm('stock', addStockForm)
}

async function addStock() {
    /*
    Attempts to add ticker to the portfolio
    */
    let ticker = document.getElementById('stock-ticker').value
    const addStockResponse = await fetch(addStockEndpoint, {
        method: "POST",
        body: JSON.stringify({ticker: ticker}),
        headers: {
            'Content-Type': 'application/json; charset=UTF-8'
        }
    })

    // Handle the response
    if (!addStockResponse.ok) {
        const error = await response.text()
        addAssetFormAlert(errorText)
    } else {
        // Re-render the stock list
        const userData = await getUserDataFromEndpoint()
        renderStocksInPortfolio(userData)

    }
    
    renderAddAssetForm('stock', addStockForm)
}

async function removeSymbolButtonOnclick(removeStockButton) {
    /*
    Removes a symbol from the portfolio.
    */
    const symbolInfoDiv = removeStockButton.closest('.symbol-info')

    const symbolElement = symbolInfoDiv.querySelector(".symbol")
    const symbol = symbolElement.textContent

    // make the parent API call
    await fetch(removeSymbolEndpoint, {
        method: "POST",
        body: JSON.stringify({symbol: symbol}),
        headers: {
            'Content-Type': 'application/json; charset=UTF-8'
        }
    })
    
    const userData = await getUserDataFromEndpoint()
    renderStocksInPortfolio(userData)
}