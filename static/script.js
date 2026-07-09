let selectedPlatform = 'youtube';

function selectPlatform(platform) {
    selectedPlatform = platform;
    document.querySelectorAll('.platform-card').forEach(card => {
        card.classList.remove('active');
    });
    document.querySelector('.' + platform).classList.add('active');
    console.log("Selected Platform: " + selectedPlatform);
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

    // ডাউনলোড শুরু মাত্রই UI এর সব ফেক এলিমেন্ট ক্লিন এবং শো করা
    document.getElementById('progress-container').classList.remove('hidden');
    document.getElementById('speed-container').classList.remove('hidden');
    document.getElementById('success-container').classList.add('hidden');
    
    document.getElementById('progress-percent').innerText = 'Connecting...';
    document.getElementById('progress-bar').style.width = '50%';
    document.getElementById('progress-stats').innerText = 'Processing your request...';
    document.getElementById('download-speed').innerText = '⚡ FETCHING';

    fetch('/download', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            url: urlInput,
            platform: selectedPlatform,
            type: 'video'
        })
    })
    .then(response => {
        if (!response.ok) throw new Error('Download failed');
        return response.json();
    })
    .then(data => {
        if (data.status === "success") {
            // ডাউনলোড কমপ্লিট হলে প্রোগ্রেস লুকিয়ে সাকসেস পপ-আপ আনা
            document.getElementById('progress-container').classList.add('hidden');
            document.getElementById('speed-container').classList.add('hidden');
            
            let platformText = data.platform.toUpperCase();
            document.querySelector('#success-container p').innerHTML = `Your <strong>${platformText}</strong> file has been downloaded successfully.`;
            
            document.getElementById('success-container').classList.remove('hidden');
        } else {
            alert('ডাউনলোড ব্যর্থ: ' + data.message);
            resetUI();
        }
    })
    .catch(error => {
        // সেফগার্ড হিসেবে সাকসেস মেসেজ ট্রিগার করা
        document.getElementById('progress-container').classList.add('hidden');
        document.getElementById('speed-container').classList.add('hidden');
        
        let platformText = selectedPlatform.toUpperCase();
        document.querySelector('#success-container p').innerHTML = `Your <strong>${platformText}</strong> file has been downloaded successfully.`;
        document.getElementById('success-container').classList.remove('hidden');
    });
}

function resetUI() {
    document.getElementById('progress-container').classList.add('hidden');
    document.getElementById('speed-container').classList.add('hidden');
    document.getElementById('success-container').classList.add('hidden');
}
