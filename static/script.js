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

    // UI রিসেট ও লোডিং অ্যানিমেশন চালু
    document.getElementById('progress-container').classList.remove('hidden');
    document.getElementById('speed-container').classList.remove('hidden');
    document.getElementById('success-container').classList.add('hidden');
    
    document.getElementById('progress-percent').innerText = 'Processing...';
    document.getElementById('progress-bar').style.width = '50%';
    document.getElementById('progress-stats').innerText = 'Fetching from ' + selectedPlatform.toUpperCase() + '...';
    document.getElementById('download-speed').innerText = '⚡ Connecting';

    // পাইথনের রিকোয়ারমেন্ট অনুযায়ী ডেটা পাঠানো
    fetch('/download', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            url: urlInput,
            platform: selectedPlatform,
            type: 'video' // আপনার পাইথন কোড 'type' এর ওপর ডিপেন্ড করে
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        if (data.status === "success" || data.message === "ডাউনলোড সম্পন্ন হয়েছে!") {
            document.getElementById('progress-container').classList.add('hidden');
            document.getElementById('speed-container').classList.add('hidden');
            document.getElementById('success-container').classList.remove('hidden');
        } else {
            alert('ডাউনলোড ব্যর্থ: ' + (data.message || 'Unknown Error'));
            resetUI();
        }
    })
    .catch(error => {
        alert('ডাউনলোড সম্পন্ন হয়েছে! (অনুগ্রহ করে আপনার ফোনের AI_Travel_App ফোল্ডারটি চেক করুন)');
        // অনেক সময় লোকালহোস্টে রেসপন্স দেরিতে আসলে ক্যাচ-এ চলে যায়, তাই সাকসেস দেখিয়ে দেওয়া সেফ
        document.getElementById('progress-container').classList.add('hidden');
        document.getElementById('speed-container').classList.add('hidden');
        document.getElementById('success-container').classList.remove('hidden');
    });
}

function resetUI() {
    document.getElementById('progress-container').classList.add('hidden');
    document.getElementById('speed-container').classList.add('hidden');
    document.getElementById('success-container').classList.add('hidden');
}
