function generateEmail() {
    const recipients = document.getElementById('recipients').value;
    const prompt = document.getElementById('prompt').value;

    fetch('/generate-email', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ recipients, prompt })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('generatedEmail').value = data.email;
    })
    .catch(error => console.error('Error:', error));
}

function sendEmail() {
    const recipients = document.getElementById('recipients').value;
    const emailContent = document.getElementById('generatedEmail').value;

    fetch('/send-email', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ recipients, emailContent })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
    })
    .catch(error => console.error('Error:', error));
}