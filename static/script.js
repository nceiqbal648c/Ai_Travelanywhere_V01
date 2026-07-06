/* ==========================================
   AI Travel Anywhere v2.0
   script.js
   Part 1 / 4
========================================== */

const urlInput = document.getElementById("video-url");
const pasteBtn = document.getElementById("paste-btn");

const mp4Btn = document.querySelector(".mp4");
const mp3Btn = document.querySelector(".mp3");

const progress = document.getElementById("progress");
const percent = document.getElementById("percent");

const title = document.getElementById("video-title");
const channel = document.getElementById("channel-name");

const thumbnail = document.getElementById("thumbnail");

/* Paste Button */

pasteBtn.addEventListener("click", async () => {

    try{

        const text = await navigator.clipboard.readText();

        urlInput.value = text;

    }

    catch(error){

        alert("Clipboard access denied.");

    }

});
/* ==========================================
   AI Travel Anywhere v2.0
   script.js
   Part 2 / 4
========================================== */

function animateProgress() {

    let value = 0;

    progress.style.width = "0%";
    percent.innerText = "0%";

    const timer = setInterval(() => {

        value += 2;

        progress.style.width = value + "%";
        percent.innerText = value + "%";

        if (value >= 100) {

            clearInterval(timer);

        }

    }, 35);

}

/* ==========================================
   AI Travel Anywhere v2.0
   script.js
   Part 3 / 4
========================================== */

/* Button Events */

mp4Btn.addEventListener("click", () => {

    startDownload("video");

});

mp3Btn.addEventListener("click", () => {

    startDownload("audio");

});

/* Enter Key Support */

urlInput.addEventListener("keydown", (event) => {

    if(event.key==="Enter"){

        startDownload("video");

    }

});

/* Auto Focus */

window.addEventListener("load",()=>{

    urlInput.focus();

});

/* Reset Progress */

function resetProgress(){

    progress.style.width="0%";

    percent.innerText="0%";

}
/* ==========================================
   AI Travel Anywhere v2.0
   script.js
   Part 4 / 4
========================================== */

/* Download File */

async function saveFile(response, type){

    const blob = await response.blob();

    const url = window.URL.createObjectURL(blob);

    const a = document.createElement("a");

    a.href = url;

    a.download = type === "audio" ? "audio.mp3" : "video.mp4";

    document.body.appendChild(a);

    a.click();

    a.remove();

    window.URL.revokeObjectURL(url);

}

/* Replace startDownload() success section */

async function downloadFile(type){

    const url = urlInput.value.trim();

    if(url===""){

        alert("Please paste a valid link.");

        return;

    }

    resetProgress();

    animateProgress();

    title.innerText="Downloading...";
    channel.innerText="Please wait...";

    try{

        const response = await fetch("/download",{

            method:"POST",

            headers:{
                "Content-Type":"application/json"
            },

            body:JSON.stringify({

                url:url,
                type:type

            })

        });

        if(!response.ok){

            throw new Error("Server Error");

        }

        await saveFile(response,type);

        title.innerText="Download Complete";

        channel.innerText="File saved successfully.";

    }

    catch(error){

        title.innerText="Download Failed";

        channel.innerText=error.message;

        alert(error.message);

    }

}

/* Final Button Connection */

mp4Btn.onclick = ()=> downloadFile("video");

mp3Btn.onclick = ()=> downloadFile("audio");
