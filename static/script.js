document.addEventListener("DOMContentLoaded", function () {
    const pasteBtn = document.getElementById("pasteBtn");
    const videoUrlInput = document.getElementById("videoUrl");
    const platformCards = document.querySelectorAll(".platform-card");
    const startDownloadBtn = document.getElementById("startDownloadBtn");
    
    const progressCard = document.getElementById("progressCard");
    const successCard = document.getElementById("successCard");
    const progressBarFill = document.getElementById("progressBarFill");

    // ১. পেস্ট বাটন ট্রিগার (ক্লিপবোর্ড থেকে লিংক রিড করার কোড)
    pasteBtn.addEventListener("click", async function () {
        try {
            const text = await navigator.clipboard.readText();
            videoUrlInput.value = text;
        } catch (err) {
            alert("Clipboard read permission denied! Paste text manually.");
        }
    });

    // ২. প্ল্যাটফর্ম কার্ড সিলেকশন টগল
    platformCards.forEach(card => {
        card.addEventListener("click", function () {
            platformCards.forEach(c => c.classList.remove("active"));
            this.classList.add("active");
        });
    });

    // ৩. মেইন ডাউনলোড বাটন ক্লিকে প্রগ্রেস অ্যানিমেশন শো
    startDownloadBtn.addEventListener("click", function () {
        if (!videoUrlInput.value.trim()) {
            alert("Please paste a target video link first!");
            return;
        }

        // রিয়েল ইন্টারফেসের মতো প্রগ্রেস বার ০ থেকে শুরু করা
        progressCard.style.display = "block";
        successCard.style.display = "none";
        progressBarFill.style.width = "0%";

        // প্রগ্রেস বার স্মুথ লোড করানোর ফেক ইন্টারভাল টাইমার
        let currentWidth = 0;
        const interval = setInterval(() => {
            currentWidth += 5;
            progressBarFill.style.width = currentWidth + "%";

            if (currentWidth >= 100) {
                clearInterval(interval);
                // প্রগ্রেস শেষ হলে সাকসেস প্যানেল কার্ড শো করা
                setTimeout(() => {
                    progressCard.style.display = "none";
                    successCard.style.display = "flex";
                }, 400);
            }
        }, 150);
    });
});
