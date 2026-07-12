function pasteLink() {
    navigator.clipboard.readText().then(text => document.getElementById('url').value = text);
}

function startDownload() {
    const url = document.getElementById('url').value;
    const loader = document.getElementById('loader');
    const status = document.getElementById('status');
    
    if(!url) return alert("Paste a link first!");
    
    loader.style.display = "block";
    status.innerText = "Downloading...";
    
    fetch('/download', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({url: url})
    })
    .then(res => res.json())
    .then(data => {
        loader.style.display = "none";
        status.innerText = "Finished";
        alert(data.message);
    })
    .catch(err => {
        loader.style.display = "none";
        status.innerText = "Error!";
        alert("Download failed.");
    });
}

