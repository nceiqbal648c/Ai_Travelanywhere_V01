async function startProcess() {
    const url = document.getElementById('video-url').value;
    const format = document.getElementById('format-select').value;
    const status = document.getElementById('status');

    if(!url) {
        alert("Link dao boss!");
        return;
    }
    
    status.innerText = "Downloading... Please wait";
    
    try {
        const res = await fetch('/download', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({url: url, format: format})
        });
        
        const data = await res.json();
        if (res.ok) {
            status.innerText = "Finished: " + data.message;
        } else {
            status.innerText = "Error: " + data.error;
        }
    } catch (error) {
        status.innerText = "Connection Error!";
    }
}
