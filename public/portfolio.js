// ENDPOINTS
const baseURL = window.location.href //ends with /
const addStockEndpoint = baseURL + 'v1/add_stock'
const removeSymbolEndpoint = baseURL + 'v1/remove_symbol'

const addNewAssetForm = document.getElementById('variable-form')
const symbolsContainer = document.getElementById('symbols-container')

// CONSTANT ADD ASSET FORMS
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

function addStockButtonOnclick() {
    renderAddAssetForm('stock', addStockForm)
}

function addStock() {
    /*
    Attempts to add ticker to the portfolio
    */
    let ticker = document.getElementById('stock-ticker').value
    console.log(ticker)
    fetch(addStockEndpoint, {
        method: "POST",
        body: JSON.stringify({ticker: ticker}),
        headers: {
            'Content-Type': 'application/json; charset=UTF-8'
        }
    })
    .then((response) => {
        if (!response.ok) {
            return response.text().then((errorText) => {
                addAssetFormAlert(errorText)
            })
        } else {
            addSymbolToContainer(ticker)
        }
        renderAddAssetForm('stock', addStockForm)
    })
}

function addSymbolToContainer(symbol) {
    // Adds ticker to html
    symbolsContainer.innerHTML += 
    `
    <div class="symbol-info sidebar-text sidebar-text-hover">
        <p class="symbol">${symbol}</p>
        <div class="ticker-buttons">
            <button onclick="removeSymbolButtonOnclick(this)">Remove</button>
        </div>
    </div>
    `
}

function removeSymbolButtonOnclick(removeStockButton) {
    /*
    Removes a symbol from the portfolio.
    */
    const symbolInfoDiv = removeStockButton.closest('.symbol-info')

    if (symbolInfoDiv) {
        const symbolElement = symbolInfoDiv.querySelector(".symbol")
        const symbol = symbolElement.textContent

        // make the parent API call
        fetch(removeSymbolEndpoint, {
            method: "POST",
            body: JSON.stringify({symbol: symbol}),
            headers: {
                'Content-Type': 'application/json; charset=UTF-8'
            }
        })
        .then((response) => {
            if (response.ok) {
                symbolInfoDiv.remove()
            }
        })
    }
}