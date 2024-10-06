<script>
    function generateQuery() {
    const sqlType = document.getElementById('sql-type').value;
    const prompt = document.getElementById('prompt-input').value;
    let query = '';

    if (prompt.toLowerCase().includes('highest paid employee')) {
        query = `SELECT * FROM employees WHERE salary = (SELECT MAX(salary) FROM employees);`;
    } else {
        query = `-- SQL query for ${sqlType} based on prompt: ${prompt}`;
    }

    document.getElementById('generated-output').innerText = query;

    // Create a new textbox
    const newTextbox = document.createElement('textarea');
    newTextbox.rows = 4;
    newTextbox.style.width = '100%';
    newTextbox.style.border = 'none';
    newTextbox.style.outline = 'none';
    newTextbox.style.resize = 'none';
    newTextbox.style.fontSize = '24px';
    newTextbox.style.fontFamily = "'Inria Sans', sans-serif";
    newTextbox.style.color = '#808080';
    newTextbox.value = query;

    // Append the new textbox to the container
    const container = document.querySelector('.main-content');
    container.appendChild(newTextbox);
}

document.addEventListener('DOMContentLoaded', () => {
    const promptInput = document.getElementById('prompt-input');
    const placeholderText = 'Enter prompt to generate query eg: give me highest paid employee';

    promptInput.value = placeholderText;
    promptInput.style.color = '#808080';

    promptInput.addEventListener('focus', () => {
        if (promptInput.value === placeholderText) {
            promptInput.value = '';
            promptInput.style.color = '#000000';
        }
    });

    promptInput.addEventListener('blur', () => {
        if (promptInput.value === '') {
            promptInput.value = placeholderText;
            promptInput.style.color = '#808080';
        }
    });
});

    </script>