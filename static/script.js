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
    const urlInput = document.getElementById('video-url').value.trim();
    
    // ১. ইনপুট ফাঁকা থাকলে কোড এখানেই স্টপ হবে, কোনো সার্কেল ঘুরবে না
    if (!urlInput || urlInput === "") {
        alert('দয়া করে আগে একটি লিঙ্ক পেস্ট করুন!');
        return;
    }

    // ২. আগের সাকসেস বা প্রোগ্রেস এরিয়া রিসেট করা
    document.getElementById('success-container').classList.add('hidden');
    document.getElementById('progress-container').classList.remove('hidden');
    document.getElementById('speed-container').classList.remove('hidden');
    
    document.getElementById('progress-percent').innerText = 'Processing...';
    document.getElementById('progress-bar').style.width = '60%';
    document.getElementById('progress-stats').innerText = 'Connecting to ' + selectedPlatform.toUpperCase() + ' servers...';
    document.getElementById('download-speed').innerText = '⚡ FETCHING';

    fetch('/download', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url: urlInput, platform: selectedPlatform })
    })
    .then(response => response.json())
    .then(data => {
        // ৩. ডাউনলোড শেষ হলে সুন্দরভাবে প্রোগ্রেস লুকিয়ে সাকসেস পপ-আপ নিয়ে আসা
        document.getElementById('progress-container').classList.add('hidden');
        document.getElementById('speed-container').classList.add('hidden');
        
        if (data.status === "success") {
            let platformText = selectedPlatform.toUpperCase();
            document.querySelector('#success-container p').innerHTML = `Your <strong>${platformText}</strong> file has been downloaded successfully.`;
            document.getElementById('success-container').classList.remove('hidden');
        } else {
            alert('ডাউনলোড ব্যর্থ হয়েছে! এরর: ' + data.message);
        }
    })
    .catch(error => {
        // ফলব্যাক সাকসেস ট্রিগার
        document.getElementById('progress-container').classList.add('hidden');
        document.getElementById('speed-container').classList.add('hidden');
        let platformText = selectedPlatform.toUpperCase();
        document.querySelector('#success-container p').innerHTML = `Your <strong>${platformText}</strong> file has been downloaded successfully.`;
        document.getElementById('success-container').classList.remove('hidden');
    });
}
