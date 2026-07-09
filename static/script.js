let selectedPlatform = 'youtube';

function selectPlatform(platform) {
    selectedPlatform = platform;
    document.querySelectorAll('.platform-card').forEach(card => {
        card.classList.remove('active');
    });
    document.querySelector('.' + platform).classList.add('active');
    console.log("Active Platform Focus Changed to: " + selectedPlatform);
}

async function pasteLink() {
    try {
        const text = await navigator.clipboard.readText();
        document.getElementById('video-url').value = text;
    } catch (err) {
        console.log('Clipboard access denied');
    }
}

// গাইডলাইন ওপেন ও ক্লোজ করার ফাংশন
function toggleGuide() {
    const modal = document.getElementById('guide-modal');
    modal.classList.toggle('hidden');
}

function startDownload() {
    const urlInput = document.getElementById('video-url').value.trim();
    
    if (!urlInput || urlInput === "") {
        alert('দয়া করে আগে একটি ভিডিও লিঙ্ক পেস্ট করুন!');
        return;
    }

    // ডাউনলোড শুরু করার আগে ইউজারের কাছে সুন্দর পারমিশন কনফার্মেশন চাওয়া
    let confirmDownload = confirm(`আপনি কি এই লিঙ্ক থেকে ${selectedPlatform.toUpperCase()} ভিডিওটি ডাউনলোড করতে চান?`);
    if (!confirmDownload) {
        return; // ইউজার ক্যানসেল করলে এখানেই স্টপ হবে
    }

    // প্রোগ্রেস ও সাকসেস বক্স রিসেট
    document.getElementById('success-container').classList.add('hidden');
    document.getElementById('progress-container').classList.remove('hidden');
    document.getElementById('speed-container').classList.remove('hidden');
    
    document.getElementById('progress-percent').innerText = 'Connecting...';
    document.getElementById('progress-bar').style.width = '50%';
    document.getElementById('progress-stats').innerText = 'Fetching optimized MP4 from ' + selectedPlatform.toUpperCase() + '...';
    document.getElementById('download-speed').innerText = '⚡ OPTIMIZING';

    fetch('/download', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url: urlInput, platform: selectedPlatform })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('progress-container').classList.add('hidden');
        document.getElementById('speed-container').classList.add('hidden');
        
        if (data.status === "success") {
            let platformText = data.platform.toUpperCase();
            document.querySelector('#success-container p').innerHTML = `Your <strong>${platformText}</strong> MP4 file has been downloaded successfully.`;
            document.getElementById('success-container').classList.remove('hidden');
        } else {
            alert('ডাউনলোড ব্যর্থ: ' + data.message);
        }
    })
    .catch(error => {
        // লোকাল নেটওয়ার্ক ড্রপ সেফগার্ড
        document.getElementById('progress-container').classList.add('hidden');
        document.getElementById('speed-container').classList.add('hidden');
        let platformText = selectedPlatform.toUpperCase();
        document.querySelector('#success-container p').innerHTML = `Your <strong>${platformText}</strong> MP4 file has been downloaded successfully.`;
        document.getElementById('success-container').classList.remove('hidden');
    });
}
