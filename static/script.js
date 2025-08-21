document.getElementById('secretForm').onsubmit = async function(event) {
    event.preventDefault();
    let formData = new FormData(event.target);

    let response = await fetch('/secret', {
        method: 'POST',
        body: formData
    });
    let res = await response.json();
    if (res.status === 'success') {
        alert('Secret saved!');
        event.target.reset();
    }
};

async function retrieveSecret() {
    let name = document.getElementById('retrieveName').value;
    let response = await fetch('/secret/' + encodeURIComponent(name));
    let res = await response.json();
    let resultDiv = document.getElementById('result');
    if (res.secret) {
        resultDiv.innerText = "Secret Value: " + res.secret;
    } else {
        resultDiv.innerText = "Secret not found!";
    }
}
