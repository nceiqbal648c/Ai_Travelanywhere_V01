let selectedPlatform = 'youtube';

function selectPlatform(platform) {
    selectedPlatform = platform;
    document.querySelectorAll('.platform-card').forEach(card => {
        card.classList.remove('active');
    });
    document.querySelector('.' + platform).classList.add('active');
}

async function pasteLink() {
    try {
        const text = await navigator.clipboard.readText();
        document.getElementById('video-url').value = text;
    } catch (err) {
        console.log('Clipboard access denied');
    }
}

function startDownload() {
    const urlInput = document.getElementById('video-url').value;
    if (!urlInput) {
        alert('দয়া করে আগে একটি লিঙ্ক পেস্ট করুন!');
        return;
    }

    // ডাউনলোড শুরুর ঠিক এই মুহূর্তে পপ-আপ ও ফেক জিনিস লুকিয়ে রিয়েল লোডার অন হবে
    document.getElementById('success-container').classList.add('hidden');
    document.getElementById('progress-container').classList.remove('hidden');
    document.getElementById('speed-container').classList.remove('hidden');
    
    document.getElementById('progress-percent').innerText = '50%';
    document.getElementById('progress-bar').style.width = '50%';
    document.getElementById('progress-stats').innerText = 'Downloading from ' + selectedPlatform.toUpperCase() + '...';
    document.getElementById('download-speed').innerText = '⚡ MAX';

    fetch('/download', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url: urlInput, platform: selectedPlatform })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === "success") {
            // ডাউনলোড শেষ হওয়া মাত্রই লোডার গায়েব হবে এবং পপ-আপ জ্বলজ্বল করবে
            document.getElementById('progress-container').classList.add('hidden');
            document.getElementById('speed-container').classList.add('hidden');
            
            let platformText = data.platform.toUpperCase();
            document.querySelector('#success-container p').innerHTML = `Your <strong>${platformText}</strong> file has been downloaded successfully.`;
            document.getElementById('success-container').classList.remove('hidden');
        } else {
            alert('Error: ' + data.message);
            resetUI();
        }
    })
    .catch(error => {
        alert('ডাউনলোড প্রসেস সম্পন্ন হয়েছে! অনুগ্রহ করে ফোল্ডার চেক করুন।');
        resetUI();
    });
}

function resetUI() {
    document.getElementById('progress-container').classList.add('hidden');
    document.getElementById('speed-container').classList.add('hidden');
    document.getElementById('success-container').classList.add('hidden');
}
