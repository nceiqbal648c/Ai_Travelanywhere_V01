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

    // ডাউনলোড শুরুর ইন্টারফেস ফ্রেশ করা
    document.getElementById('progress-container').classList.remove('hidden');
    document.getElementById('speed-container').classList.remove('hidden');
    document.getElementById('success-container').classList.add('hidden');
    
    document.getElementById('progress-percent').innerText = 'Processing...';
    document.getElementById('progress-bar').style.width = '50%'; // লোডিং বোঝানোর জন্য ৫০% বর্ডার করা
    document.getElementById('progress-stats').innerText = 'Downloading from ' + selectedPlatform + '...';
    document.getElementById('download-speed').innerText = '⚡ Fast';

    fetch('/download', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            url: urlInput,
            type: 'video'
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === "success") {
            // ডাউনলোড একদম শেষ হলে সাকসেস দেখানো
            document.getElementById('progress-container').classList.add('hidden');
            document.getElementById('speed-container').classList.add('hidden');
            document.getElementById('success-container').classList.remove('hidden');
        } else {
            alert('ডাউনলোড ব্যর্থ হয়েছে: ' + (data.message || 'Unknown Error'));
            resetUI();
        }
    })
    .catch(error => {
        alert('সার্ভারে সমস্যা হয়েছে! অনুগ্রহ করে আবার চেষ্টা করুন।');
        resetUI();
    });
}

function resetUI() {
    document.getElementById('progress-container').classList.add('hidden');
    document.getElementById('speed-container').classList.add('hidden');
    document.getElementById('success-container').classList.add('hidden');
}
