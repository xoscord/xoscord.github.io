let audioCtx;
let oscillator;
let gainNode;
let isPlaying = false;

const freqSlider = document.getElementById("freqSlider");
const freqValue = document.getElementById("freqValue");
const volumeSlider = document.getElementById("volumeSlider");
const waveSelect = document.getElementById("waveSelect");
const playBtn = document.getElementById("playBtn");

// Initialize audio controls
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
        playBtn.style.background = "skyblue";
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

// Custom dropdown functionality - SIMPLIFIED VERSION
document.addEventListener('DOMContentLoaded', function() {
    const selectTrigger = document.querySelector('.select-trigger');
    const selectedValue = document.querySelector('.selected-value');
    const selectOptions = document.querySelector('.select-options');
    const options = document.querySelectorAll('.option');
    const originalSelect = document.getElementById('waveSelect');

    // Check if elements exist
    if (!selectTrigger || !selectedValue || !selectOptions || !originalSelect) {
        console.log('Some dropdown elements not found, but continuing...');
        return;
    }

    // Simple initialization
    function initializeDropdown() {
        const currentValue = originalSelect.value;
        const currentText = originalSelect.options[originalSelect.selectedIndex].text;
        selectedValue.textContent = currentText;
    }

    // Toggle dropdown
    selectTrigger.addEventListener('click', function(e) {
        e.stopPropagation();
        const isOpen = selectOptions.classList.contains('show');
        
        if (isOpen) {
            selectOptions.classList.remove('show');
            selectTrigger.classList.remove('active');
        } else {
            selectOptions.classList.add('show');
            selectTrigger.classList.add('active');
        }
    });

    // Handle option selection - SIMPLIFIED
    options.forEach(option => {
        option.addEventListener('click', function(e) {
            const value = this.getAttribute('data-value');
            const text = this.textContent;
            
            // Update UI
            selectedValue.textContent = text;
            
            // Update the hidden select
            originalSelect.value = value;
            
            // Trigger the audio change
            if (oscillator) {
                oscillator.type = value;
            }
            
            // Close dropdown
            selectOptions.classList.remove('show');
            selectTrigger.classList.remove('active');
            
            console.log('Waveform changed to:', value);
        });
    });

    // Close dropdown when clicking outside
    document.addEventListener('click', function(e) {
        if (!selectTrigger.contains(e.target) && !selectOptions.contains(e.target)) {
            selectOptions.classList.remove('show');
            selectTrigger.classList.remove('active');
        }
    });

    // Close on escape
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            selectOptions.classList.remove('show');
            selectTrigger.classList.remove('active');
        }
    });

    // Initialize
    initializeDropdown();
    console.log('Custom dropdown initialized');
});

// Fallback: If DOM is already loaded, initialize
if (document.readyState === 'complete' || document.readyState === 'interactive') {
    setTimeout(() => {
        // Trigger any existing DOMContentLoaded events
    }, 1);
}





// Lock horizontal scrolling for dropdown options
function lockDropdownScrolling() {
    const selectOptions = document.querySelector('.select-options');
    
    if (!selectOptions) return;
    
    // Prevent horizontal scrolling with wheel/trackpad
    selectOptions.addEventListener('wheel', function(e) {
        if (e.deltaX !== 0) {
            e.preventDefault();
        }
    }, { passive: false });
    
    // Prevent horizontal scrolling with touch
    let startX = 0;
    selectOptions.addEventListener('touchstart', function(e) {
        startX = e.touches[0].clientX;
    }, { passive: true });
    
    selectOptions.addEventListener('touchmove', function(e) {
        if (e.touches.length > 0) {
            const currentX = e.touches[0].clientX;
            // If horizontal movement is detected, prevent it
            if (Math.abs(currentX - startX) > 10) {
                e.preventDefault();
            }
        }
    }, { passive: false });
    
    // Prevent keyboard horizontal scrolling
    selectOptions.addEventListener('keydown', function(e) {
        if (e.key === 'ArrowLeft' || e.key === 'ArrowRight') {
            e.preventDefault();
        }
    });
}

// Initialize when page loads
document.addEventListener('DOMContentLoaded', function() {
    lockDropdownScrolling();
});
