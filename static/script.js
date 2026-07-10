function startDownload() {
    let url = document.getElementById('video-url').value;
    if (confirm("আপনি কি এই লিঙ্ক থেকে YOUTUBE ভিডিওটি ডাউনলোড করতে চান?")) {
        fetch('/download', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({url: url})
        })
        .then(res => res.json())
        .then(data => alert(data.message));
    }
}
