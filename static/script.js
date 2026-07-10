async function pasteUrl() {
    const text = await navigator.clipboard.readText();
    document.getElementById('video-url').value = text;
}

async function startProcess() {
    const url = document.getElementById('video-url').value;
    if (!url) {
        alert("আগে লিঙ্ক পেস্ট করুন!");
        return;
    }

    const startBtn = document.querySelector('.start-btn');
    startBtn.innerText = "ডাউনলোড হচ্ছে...";
    startBtn.disabled = true;

    const res = await fetch('/download', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({url: url})
    });
    
    const data = await res.json();
    
    startBtn.innerText = "START";
    startBtn.disabled = false;
    
    alert(data.message || data.error);
}
