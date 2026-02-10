let audioCtx;
let oscillator;
let gainNode;
let isPlaying = false;

const freqSlider = document.getElementById("freqSlider");
const freqValue = document.getElementById("freqValue");
const volumeSlider = document.getElementById("volumeSlider");
const waveSelect = document.getElementById("waveSelect");
const playBtn = document.getElementById("playBtn");

freqSlider.oninput = () => {
    freqValue.textContent = freqSlider.value;
    if (oscillator) oscillator.frequency.value = freqSlider.value;
};

volumeSlider.oninput = () => {
    if (gainNode) gainNode.gain.value = volumeSlider.value;
};

waveSelect.oninput = () => {
    if (oscillator) oscillator.type = waveSelect.value;
};

playBtn.onclick = () => {
    if (!isPlaying) {
        startToneSmooth();
        playBtn.textContent = "Stop";
        playBtn.style.background = "#e53935";
    } else {
        stopToneSmooth();
        playBtn.textContent = "Start";
        playBtn.style.background = "#4CAF50";
    }
    isPlaying = !isPlaying;
};

function startToneSmooth() {
    audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    oscillator = audioCtx.createOscillator();
    gainNode = audioCtx.createGain();

    oscillator.type = waveSelect.value;
    oscillator.frequency.value = freqSlider.value;

    // Start silent first
    gainNode.gain.setValueAtTime(0, audioCtx.currentTime);

    oscillator.connect(gainNode);
    gainNode.connect(audioCtx.destination);

    oscillator.start();

    // Smooth fade-in (0.4 seconds)
    gainNode.gain.linearRampToValueAtTime(volumeSlider.value, audioCtx.currentTime + 0.4);
}

function stopToneSmooth() {
    if (!gainNode || !audioCtx) return;

    // Smooth fade-out (0.4 seconds)
    gainNode.gain.cancelScheduledValues(audioCtx.currentTime);
    gainNode.gain.setValueAtTime(gainNode.gain.value, audioCtx.currentTime);
    gainNode.gain.linearRampToValueAtTime(0, audioCtx.currentTime + 0.4);

    // Stop oscillator after fade
    setTimeout(() => {
        if (oscillator) oscillator.stop();
        if (audioCtx) audioCtx.close();
    }, 400);
}

