const input = document.getElementById('urlInput');
const processBtn = document.getElementById('processBtn');
const resultContainer = document.getElementById('resultContainer');
const msg = document.getElementById('message');
const thumbnail = document.getElementById('videoThumbnail');
const title = document.getElementById('videoTitle');
const qualitySelect = document.getElementById('qualitySelect');
const progressContainer = document.getElementById('progressContainer');
const progressFill = document.getElementById('progressFill');
const progressText = document.getElementById('progressText');
const historyList = document.getElementById('historyList');
const historyContainer = document.getElementById('historyContainer');

// Load history on startup
document.addEventListener('DOMContentLoaded', loadHistory);

async function processLink() {
    const url = input.value.trim();
    if (!url) {
        showError("Please paste a link first.");
        return;
    }

    // Reset UI
    msg.textContent = "Fetching info...";
    msg.className = "message";
    processBtn.classList.add('loading');
    resultContainer.style.display = 'none';
    progressContainer.style.display = 'none';
    input.disabled = true;
    processBtn.disabled = true;

    try {
        const response = await fetch('/get-info', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url: url })
        });

        const data = await response.json();

        if (data.success) {
            msg.textContent = "";
            showResult(data.info);
        } else {
            showError(data.error);
        }
    } catch (error) {
        showError("Network error. " + error);
    } finally {
        processBtn.classList.remove('loading');
        input.disabled = false;
        processBtn.disabled = false;
    }
}

function showResult(info) {
    thumbnail.src = info.thumbnail;
    title.textContent = info.title;

    // Clear options
    qualitySelect.innerHTML = "";

    // Populate options
    info.formats.forEach(fmt => {
        const option = document.createElement('option');
        option.value = fmt.id;
        option.textContent = fmt.label;
        qualitySelect.appendChild(option);
    });

    // Add Auto/Best option
    const autoOption = document.createElement('option');
    autoOption.value = "";
    autoOption.textContent = "Auto / Best Quality";
    autoOption.selected = true;
    qualitySelect.insertBefore(autoOption, qualitySelect.firstChild);

    resultContainer.style.display = 'block';

    // Store current video info for history
    window.currentVideoInfo = info;
}

function generateUUID() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
        var r = Math.random() * 16 | 0, v = c == 'x' ? r : (r & 0x3 | 0x8);
        return v.toString(16);
    });
}

async function startDownload(type = 'video') {
    const url = input.value.trim();
    let formatId = qualitySelect.value;

    if (type === 'audio') {
        formatId = 'audio';
    }

    const downloadBtn = document.getElementById('downloadBtn');
    const audioBtn = document.getElementById('audioBtn');

    const downloadId = generateUUID();

    msg.textContent = type === 'audio' ? "Converting to Audio..." : "Downloading...";
    msg.className = "message";

    downloadBtn.disabled = true;
    audioBtn.disabled = true;

    progressContainer.style.display = 'block';
    progressFill.style.width = '0%';
    progressText.textContent = '0%';

    // Start Polling
    const pollInterval = setInterval(async () => {
        try {
            const res = await fetch(`/progress/${downloadId}`);
            const data = await res.json();
            if (data.status !== "Not found") {
                progressFill.style.width = data.percent + '%';
                progressText.textContent = `${Math.round(data.percent)}% - ${data.status}`;
            }
        } catch (e) { console.log("Poll error", e); }
    }, 1000);

    try {
        const response = await fetch('/download', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                url: url,
                format_id: formatId,
                download_id: downloadId
            })
        });

        if (response.ok) {
            clearInterval(pollInterval);
            progressFill.style.width = '100%';
            progressText.textContent = '100% - Complete!';

            // It's a file blob
            const blob = await response.blob();
            const downloadUrl = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = downloadUrl;

            // Try to get filename
            const disposition = response.headers.get('Content-Disposition');
            let filename = type === 'audio' ? "audio.mp3" : "video.mp4";
            if (disposition && disposition.indexOf('attachment') !== -1) {
                const filenameRegex = /filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/;
                const matches = filenameRegex.exec(disposition);
                if (matches != null && matches[1]) {
                    filename = matches[1].replace(/['"]/g, '');
                }
            }

            a.download = filename;
            document.body.appendChild(a);
            a.click();
            a.remove();
            window.URL.revokeObjectURL(downloadUrl);

            msg.textContent = "Download complete!";
            msg.className = "message success";

            // Save to history
            addToHistory(window.currentVideoInfo, type);

        } else {
            clearInterval(pollInterval);
            const data = await response.json();
            showError(data.error || "Download failed.");
        }
    } catch (error) {
        clearInterval(pollInterval);
        showError("An error occurred during download.");
        console.error(error);
    } finally {
        downloadBtn.disabled = false;
        audioBtn.disabled = false;
    }
}

function addToHistory(info, type) {
    if (!info) return;

    const item = {
        title: info.title,
        thumbnail: info.thumbnail,
        url: input.value,
        type: type,
        date: new Date().toLocaleDateString()
    };

    let history = JSON.parse(localStorage.getItem('dl_history') || '[]');
    history.unshift(item);
    if (history.length > 5) history.pop(); // Keep last 5
    localStorage.setItem('dl_history', JSON.stringify(history));

    loadHistory();
}

function loadHistory() {
    let history = JSON.parse(localStorage.getItem('dl_history') || '[]');
    historyList.innerHTML = "";

    if (history.length > 0) {
        historyContainer.style.display = 'block';
        history.forEach(item => {
            const div = document.createElement('div');
            div.className = 'history-item';
            div.innerHTML = `
                <img src="${item.thumbnail}" class="history-thumb">
                <div class="history-info">
                    <div class="history-title">${item.title}</div>
                    <div class="history-date">${item.type.toUpperCase()} • ${item.date}</div>
                </div>
                <a href="#" class="history-link" onclick="input.value='${item.url}'; processLink(); return false;">
                    ↻
                </a>
            `;
            historyList.appendChild(div);
        });
    } else {
        historyContainer.style.display = 'none';
    }
}

function showError(text) {
    msg.textContent = text;
    msg.className = "message error";
}
