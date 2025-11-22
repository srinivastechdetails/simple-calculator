let currentInput = '0';
let previousInput = null;
let operation = null;
let shouldResetDisplay = false;

const displayElement = document.getElementById('display');

function updateDisplay() {
    displayElement.textContent = currentInput;
}

function appendNumber(number) {
    if (shouldResetDisplay) {
        currentInput = '';
        shouldResetDisplay = false;
    }
    if (currentInput === '0' && number !== '.') {
        currentInput = number;
    } else {
        if (number === '.' && currentInput.includes('.')) return;
        currentInput += number;
    }
    updateDisplay();
}

function setOperation(op) {
    if (operation !== null) calculate();
    previousInput = currentInput;
    operation = op;
    shouldResetDisplay = true;
}

async function calculate() {
    if (operation === null || shouldResetDisplay) return;

    const num1 = parseFloat(previousInput);
    const num2 = parseFloat(currentInput);

    // Show spinner while waiting for the response
    document.getElementById('spinner').style.display = 'block';
    // Hide any previous error message
    document.getElementById('error').style.display = 'none';

    try {
        const response = await fetch(`/${operation}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ a: num1, b: num2 })
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Error');
        }

        const data = await response.json();
        currentInput = data.result.toString();
        operation = null;
        shouldResetDisplay = true; // Ready for new calculation or chaining
        updateDisplay();
    } catch (error) {
        // Show error message to the user
        const errorDiv = document.getElementById('error');
        errorDiv.textContent = error.message;
        errorDiv.style.display = 'block';
        currentInput = 'Error';
        updateDisplay();
        setTimeout(() => {
            currentInput = '0';
            shouldResetDisplay = true;
            updateDisplay();
        }, 2000);
    } finally {
        // Hide spinner after request completes (both success and error)
        document.getElementById('spinner').style.display = 'none';
    }
}
