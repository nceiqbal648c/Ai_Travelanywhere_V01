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

// 🔐 অ্যাডমিন সিক্রেট আপলোড ট্রিগার (কার্ডে ডাবল ক্লিক করলে প্রম্পট আসবে)
function triggerAdminUpload() {
    const password = prompt("অনুগ্রহ করে সিক্রেট অ্যাডমিন পাসওয়ার্ড দিন:");
    if (password === null) return; 
    
    if (password === "1234") { 
        document.getElementById('admin-image-input').click(); 
    } else {
        alert("ভুল পাসওয়ার্ড! আপনি ছবি পরিবর্তন করতে পারবেন না।");
    }
}

// 🚀 গ্যালারি থেকে ছবি সিলেক্ট করার পর আপলোড লজিক
function handleAdminImageUpload(input) {
    if (!input.files || !input.files[0]) return;
    
    const formData = new FormData();
    formData.append('image', input.files[0]);
    formData.append('password', '1234'); 
    
    fetch('/admin/upload-profile', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            alert(data.message);
            document.getElementById('profile-display-img').src = '/static/profile.jpg?t=' + new Date().getTime();
        } else {
            alert('ত্রুটি: ' + data.message);
        }
    })
    .catch(error => {
        console.error('Upload Error:', error);
        alert('ছবি আপলোড করতে সমস্যা হয়েছে!');
    });
}

function startDownload() {
    const urlInput = document.getElementById('video-url').value.trim();
    if (!urlInput) {
        alert('দয়া করে আগে একটি ভিডিও লিঙ্ক পেস্ট করুন!');
        return;
    }

    let displayPlatform = selectedPlatform.toUpperCase();
    if(selectedPlatform === 'facebook') displayPlatform = 'FACEBOOK REEL';
    
    let confirmDownload = confirm(`আপনি কি এই লিঙ্ক থেকে ${displayPlatform} ভিডিওটি ডাউনলোড করতে চান?`);
    if (!confirmDownload) return;

    // নতুন ডাউনলোডের শুরুতে আগের সাকসেস মেসেজ ও স্পিড কার্ড রিসেট করা
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
        // ডাউনলোড শেষ হলে প্রোগ্রেস ও স্পিড হাইড করা
        document.getElementById('progress-container').classList.add('hidden');
        document.getElementById('speed-container').classList.add('hidden');
        
        if (data.status === "success") {
            document.querySelector('#success-container p').innerHTML = `Your <strong>${displayPlatform}</strong> MP4 file has been downloaded successfully.`;
            document.getElementById('success-container').classList.remove('hidden');
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
