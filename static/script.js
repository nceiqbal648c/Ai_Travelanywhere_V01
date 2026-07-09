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

function toggleGuide() {
    const modal = document.getElementById('guide-modal');
    if (modal.classList.contains('hidden')) {
        modal.classList.remove('hidden');
        modal.style.display = 'flex';
    } else {
        modal.classList.add('hidden');
        modal.style.display = 'none';
    }
}

window.onclick = function(event) {
    const modal = document.getElementById('guide-modal');
    if (event.target == modal) {
        modal.classList.add('hidden');
        modal.style.display = 'none';
    }
}

function startDownload() {
    const urlInput = document.getElementById('video-url').value.trim();
    
    if (!urlInput || urlInput === "") {
        alert('দয়া করে আগে একটি ভিডিও লিঙ্ক পেস্ট করুন!');
        return;
    }

    let displayPlatform = selectedPlatform.toUpperCase();
    if(selectedPlatform === 'facebook') displayPlatform = 'FACEBOOK REEL';
    
    let confirmDownload = confirm(`আপনি কি এই লিঙ্ক থেকে ${displayPlatform} ভিডিওটি ডাউনলোড করতে চান?`);
    if (!confirmDownload) return;

    document.getElementById('success-container').classList.add('hidden');
    document.getElementById('progress-container').classList.remove('hidden');
    document.getElementById('speed-container').classList.remove('hidden');
    
    document.getElementById('progress-percent').innerText = 'Connecting...';
    document.getElementById('progress-bar').style.width = '45%';
    document.getElementById('progress-stats').innerText = 'Fetching optimized MP4 from ' + displayPlatform + '...';
    document.getElementById('download-speed').innerText = '⚡ OPTIMIZING';

    fetch('/download', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url: urlInput, platform: selectedPlatform })
    })
    .then(response => response.json())
    .then(data => {
        // ডাউনলোড শেষ হওয়া মাত্রই স্পিড কম্পোনেন্ট এবং প্রোগ্রেস বার একসাথে গায়েব হবে
        document.getElementById('progress-container').classList.add('hidden');
        document.getElementById('speed-container').classList.add('hidden');
        
        if (data.status === "success") {
            document.querySelector('#success-container p').innerHTML = `Your <strong>${displayPlatform}</strong> MP4 file has been downloaded successfully.`;
            document.getElementById('success-container').classList.remove('hidden');
            
            // ব্রাউজার ডাউনলোড ট্রিগার
            window.location.href = data.file_url;
        } else {
            alert('ডাউনলোড ব্যর্থ: ' + data.message);
        }
    })
    .catch(error => {
        document.getElementById('progress-container').classList.add('hidden');
        document.getElementById('speed-container').classList.add('hidden');
        alert('সার্ভার প্রসেস রেডি! ফাইল স্টোরেজ চেক করুন।');
    });
}
