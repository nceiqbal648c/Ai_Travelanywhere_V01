async function pasteUrl() {
    const text = await navigator.clipboard.readText();
    document.getElementById('video-url').value = text;
}

async function startProcess() {
    const url = document.getElementById('video-url').value;
    const res = await fetch('/download', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({url: url})
    });
    const data = await res.json();
    alert(data.message || data.error);
}

