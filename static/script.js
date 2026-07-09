let selectedPlatform = 'youtube';

// প্ল্যাটফর্ম সিলেক্ট করার লজিক
function selectPlatform(platform) {
    selectedPlatform = platform;
    document.querySelectorAll('.platform-card').forEach(card => {
        card.classList.remove('active');
    });
    document.querySelector('.' + platform).classList.add('active');
}

// ক্লিপবোর্ড থেকে লিঙ্ক পেস্ট করার লজিক
async function pasteLink() {
    try {
        const text = await navigator.clipboard.readText();
        document.getElementById('video-url').value = text;
    } catch (err) {
        // যদি পারমিশন না থাকে তবে ম্যানুয়ালি করতে বলবে
        console.log('Clipboard access denied');
    }
}

// আসল ডাউনলোড লজিক যা পাইথনের সাথে কথা বলবে
function startDownload() {
    const urlInput = document.getElementById('video-url').value;
    
    if (!urlInput) {
        alert('দয়া করে আগে একটি লিঙ্ক পেস্ট করুন!');
        return;
    }

    // UI এর প্রোগ্রেস ও স্পিড সেকশন শো করা
    document.getElementById('progress-container').classList.remove('hidden');
    document.getElementById('speed-container').classList.remove('hidden');
    document.getElementById('success-container').classList.add('hidden');

    // পাইথন Flask ব্যাকএন্ডে ডেটা পাঠানো
    fetch('/download', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            url: urlInput,
            type: 'video' // আপনার পাইথন কোড dl_type == 'audio' ছাড়া বাকি সব ভিডিও হিসেবে ধরে
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Download failed');
        }
        return response.json();
    })
    .then(data => {
        // ডাউনলোড সফল হলে সাকসেস মেসেজ দেখানো
        document.getElementById('progress-container').classList.add('hidden');
        document.getElementById('speed-container').classList.add('hidden');
        document.getElementById('success-container').classList.remove('hidden');
    })
    .catch(error => {
        alert('ডাউনলোড করতে সমস্যা হয়েছে! লিঙ্কটি আবার চেক করুন।');
        document.getElementById('progress-container').classList.add('hidden');
        document.getElementById('speed-container').classList.add('hidden');
    });
}
