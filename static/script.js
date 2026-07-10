let selectedPlatform = 'youtube';
function setPlatform(p) { selectedPlatform = p; alert(p.toUpperCase() + " মোড সক্রিয়!"); }
async function pasteUrl() {
    try {
        const text = await navigator.clipboard.readText();
        document.getElementById('video-url').value = text;
    } catch (err) { alert("পেস্ট করা গেল না!"); }
}
function startDownload() {
    let url = document.getElementById('video-url').value;
    if(!url) { alert("লিঙ্ক দিন!"); return; }
    fetch('/download', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({url: url, platform: selectedPlatform})
    })
    .then(res => res.json())
    .then(data => alert(data.message));
}
