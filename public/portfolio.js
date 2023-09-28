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
    let itemsToAppend = []
    let userSymbolList = userDataJson.portfolio.symbols
    for (let i=0; i < userSymbolList.length; i++) {
        let data = userSymbolList[i]
        if (typeof data !== 'object') {
            // Data is just a ticker, render appropriately
            const symbolInfoDiv = document.createElement('div')
            symbolInfoDiv.classList.add('symbol-info', 'sidebar-text', 'sidebar-text-hover')
            symbolInfoDiv.innerHTML = 
            `
            <p class="symbol">${data}</p>
                <div class="ticker-buttons">
                    <button onclick="removeSymbolButtonOnclick(this)">Remove</button>
            </div>
            `
            itemsToAppend.push(symbolInfoDiv)
        } else {
            // Data is a category, containing tickers
            const title = data.title
            const color = data.color
            const symbols = data.symbols
            
            const categoryDiv = document.createElement('div')
            categoryDiv.classList.add('symbol-category')

            const categoryButtonsDiv = document.createElement('div')
            categoryButtonsDiv.classList.add('category-buttons')
            categoryButtonsDiv.innerHTML = 
            `
            <p class="category-title">${title}</p>
            <button class="category-remove-button">Remove</button>
            `
            categoryDiv.append(categoryButtonsDiv)

            // Add all tickers to the category
            for (let i = 0; i < symbols.length; i++) {
                const symbolDiv = document.createElement('div')
                symbolDiv.classList.add('symbol-info', 'sidebar-text', 'sidebar-text-hover')
                symbolDiv.innerHTML = 
                `
                <p class="symbol">${symbols[i]}</p>
                <div class="ticker-buttons">
                    <button onclick="alert('not implemented')">Remove</button>
                </div>
                `
                categoryDiv.append(symbolDiv)
            }
            categoryDiv.style.backgroundColor = color
            itemsToAppend.push(categoryDiv)
        }
    }
    symbolsList.innerHTML = ''
    symbolsList.append(...itemsToAppend)
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
        const error = await addStockResponse.text()
        addAssetFormAlert(error)
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