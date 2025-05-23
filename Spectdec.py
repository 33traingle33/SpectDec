<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dynamic Spectrograph</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        /* Custom styles for better visual appeal and responsiveness */
        body {
            font-family: 'Inter', sans-serif;
            background-color: #1a202c; /* Dark background */
            color: #e2e8f0; /* Light text */
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            padding: 1rem;
        }
        .container {
            background-color: #2d3748; /* Slightly lighter dark background for container */
            border-radius: 0.75rem; /* Rounded corners */
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05); /* Subtle shadow */
            padding: 2rem;
            width: 100%;
            max-width: 960px; /* Max width for desktop */
            display: flex;
            flex-direction: column;
            gap: 1.5rem;
        }
        canvas {
            background-color: #000; /* Black background for spectrograph */
            border-radius: 0.5rem;
            width: 100%; /* Make canvas responsive */
            height: 400px; /* Fixed height for the spectrograph */
            border: 1px solid #4a5568;
        }
        input[type="range"]::-webkit-slider-thumb {
            -webkit-appearance: none;
            appearance: none;
            width: 16px;
            height: 16px;
            border-radius: 50%;
            background: #63b3ed; /* Blue thumb */
            cursor: pointer;
            box-shadow: 0 0 0 3px rgba(99, 179, 237, 0.5);
            margin-top: -6px; /* Adjust thumb position */
        }
        input[type="range"]::-moz-range-thumb {
            width: 16px;
            height: 16px;
            border-radius: 50%;
            background: #63b3ed;
            cursor: pointer;
            box-shadow: 0 0 0 3px rgba(99, 179, 237, 0.5);
        }
        input[type="range"] {
            -webkit-appearance: none;
            width: 100%;
            height: 4px;
            background: #4a5568; /* Slider track color */
            outline: none;
            opacity: 0.7;
            transition: opacity .2s;
            border-radius: 2px;
        }
        input[type="range"]:hover {
            opacity: 1;
        }
        .control-group {
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
        }
        .control-group label {
            font-weight: bold;
            color: #a0aec0;
        }
        .control-group span {
            font-size: 0.875rem;
            color: #cbd5e0;
        }
        .record-button.recording {
            background-color: #ef4444; /* Red for recording */
            animation: pulse 1s infinite alternate;
        }
        @keyframes pulse {
            from { transform: scale(1); opacity: 1; }
            to { transform: scale(1.02); opacity: 0.8; }
        }
        .freq-input-group {
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        .freq-input-group input[type="number"] {
            width: 80px; /* Fixed width for number input */
            padding: 0.5rem;
            border-radius: 0.375rem;
            border: 1px solid #4a5568;
            background-color: #2d3748;
            color: #e2e8f0;
            text-align: center;
        }
    </style>
</head>
<body class="bg-gray-900 text-gray-100 flex items-center justify-center min-h-screen p-4">
    <div class="container bg-gray-800 rounded-xl shadow-lg p-8 flex flex-col gap-6">
        <h1 class="text-3xl font-extrabold text-center text-blue-400 mb-4">Dynamic Audio Spectrograph</h1>

        <div class="flex flex-col items-center gap-4">
            <label for="audioFile" class="block text-lg font-medium text-gray-300">Upload Audio File:</label>
            <input type="file" id="audioFile" accept="audio/*" class="w-full max-w-md p-3 border border-gray-600 rounded-lg bg-gray-700 text-gray-200 cursor-pointer hover:border-blue-500 transition duration-300 ease-in-out">
            <button id="startMicrophone" class="w-full max-w-md p-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition duration-300 ease-in-out mt-2">
                Record from Microphone
            </button>
            <p id="statusMessage" class="text-sm text-gray-400 mt-2">Please upload an audio file or record from microphone to begin.</p>
        </div>

        <div class="flex justify-center gap-4 mt-4">
            <button id="startRecording" class="px-6 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 transition duration-300 ease-in-out record-button">
                Start Recording
            </button>
            <button id="stopRecording" class="px-6 py-3 bg-red-600 text-white rounded-lg hover:bg-red-700 transition duration-300 ease-in-out" disabled>
                Stop Recording
            </button>
            <button id="saveSpectrogramBtn" class="px-6 py-3 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition duration-300 ease-in-out">
                Save Spectrogram Image
            </button>
            <button id="stopAllAudioBtn" class="px-6 py-3 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition duration-300 ease-in-out" disabled>
                Stop All Audio
            </button>
        </div>

        <div class="text-center text-2xl font-bold text-yellow-300 mt-4">
            Detected Note: <span id="detectedNote">N/A</span>
        </div>

        <canvas id="spectrographCanvas" class="rounded-lg border border-gray-700"></canvas>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mt-4">
            <div class="control-group">
                <label for="minFreq">Minimum Frequency:</label>
                <div class="freq-input-group">
                    <input type="range" id="minFreq" min="0" max="20000" value="0" step="10">
                    <input type="number" id="minFreqNumber" min="0" max="20000" value="0" step="10">
                    <span id="minFreqValue" class="text-right">Hz</span>
                </div>
            </div>
            <div class="control-group">
                <label for="maxFreq">Maximum Frequency:</label>
                <div class="freq-input-group">
                    <input type="range" id="maxFreq" min="0" max="20000" value="20000" step="10">
                    <input type="number" id="maxFreqNumber" min="0" max="20000" value="20000" step="10">
                    <span id="maxFreqValue" class="text-right">Hz</span>
                </div>
            </div>
        </div>

        <div class="flex justify-center gap-4 mt-4">
            <button id="setA432HzBtn" class="px-6 py-3 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition duration-300 ease-in-out">
                Set Freq to A4=432 Hz
            </button>
        </div>

        <div id="messageBox" class="hidden fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <div class="bg-gray-700 p-6 rounded-lg shadow-xl text-center flex flex-col items-center gap-4">
                <p id="messageText" class="text-lg text-gray-100"></p>
                <button id="closeMessageBox" class="px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition duration-300 ease-in-out">OK</button>
            </div>
        </div>
    </div>

    <script>
        // Get DOM elements
        const audioFile = document.getElementById('audioFile');
        const startMicrophoneBtn = document.getElementById('startMicrophone');
        const startRecordingBtn = document.getElementById('startRecording');
        const stopRecordingBtn = document.getElementById('stopRecording');
        const saveSpectrogramBtn = document.getElementById('saveSpectrogramBtn');
        const stopAllAudioBtn = document.getElementById('stopAllAudioBtn');
        const spectrographCanvas = document.getElementById('spectrographCanvas');
        const minFreqSlider = document.getElementById('minFreq');
        const maxFreqSlider = document.getElementById('maxFreq');
        const minFreqNumberInput = document.getElementById('minFreqNumber');
        const maxFreqNumberInput = document.getElementById('maxFreqNumber');
        const minFreqValueSpan = document.getElementById('minFreqValue');
        const maxFreqValueSpan = document.getElementById('maxFreqValue');
        const statusMessage = document.getElementById('statusMessage');
        const detectedNoteSpan = document.getElementById('detectedNote');
        const setA432HzBtn = document.getElementById('setA432HzBtn');
        const messageBox = document.getElementById('messageBox');
        const messageText = document.getElementById('messageText');
        const closeMessageBox = document.getElementById('closeMessageBox');

        // Canvas context
        const ctx = spectrographCanvas.getContext('2d');

        // AudioContext and nodes
        let audioContext;
        let analyser;
        let fileSource = null;
        let micSource = null;
        let mediaStream = null;
        let mediaRecorder = null;
        let recordedChunks = [];
        let isRecording = false;

        // Spectrograph drawing parameters
        const barWidth = 1;
        let animationFrameId;

        // Musical note mapping
        const noteNames = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"];
        const A4_FREQUENCY = 432; // A4 note is 440 Hz

        // --- Configurable Settings for Dominant Note Indicator ---
        let dominantFreqLineColor = '#FFD700'; // Gold color
        let dominantFreqLineWidth = 1.5;
        let dominantFreqLabelColor = '#FFD700'; // Gold text
        let dominantFreqLabelFont = 'bold 14px Inter'; // Larger and bold font
        let dominantFreqLabelOffsetX = -5; // Offset from right edge
        let dominantFreqLabelOffsetY = -5; // Offset from the line itself
        // --- End Configurable Settings ---

        // Function to convert frequency to musical note
        function getNoteFromFrequency(frequency) {
            if (frequency <= 0) return "N/A";

            const semitonesFromA4 = 12 * Math.log2(frequency / A4_FREQUENCY);
            const roundedSemitones = Math.round(semitonesFromA4);
            const noteIndex = (9 + roundedSemitones % 12 + 12) % 12;
            const octave = Math.floor(4 + (roundedSemitones + 9) / 12);

            return noteNames[noteIndex] + octave;
        }

        // Function to show custom message box
        function showMessageBox(message) {
            messageText.textContent = message;
            messageBox.classList.remove('hidden');
        }

        // Close message box
        closeMessageBox.addEventListener('click', () => {
            messageBox.classList.add('hidden');
        });

        // Initialize AudioContext (handle browser compatibility)
        function initAudioContext() {
            if (!audioContext) {
                audioContext = new (window.AudioContext || window.webkitAudioContext)();
                analyser = audioContext.createAnalyser();
                analyser.fftSize = 2048;
            }
        }

        // Function to stop all active audio sources and recording
        function stopAllSources() {
            if (fileSource) {
                fileSource.stop();
                fileSource.disconnect();
                fileSource = null;
            }
            if (micSource) {
                micSource.disconnect();
                micSource = null;
            }
            if (mediaStream) {
                mediaStream.getTracks().forEach(track => track.stop());
                mediaStream = null;
            }
            if (animationFrameId) {
                cancelAnimationFrame(animationFrameId);
                animationFrameId = null;
            }
            if (isRecording && mediaRecorder) {
                mediaRecorder.stop();
                isRecording = false;
                startRecordingBtn.classList.remove('recording');
            }
            // Clear canvas when stopping sources
            ctx.clearRect(0, 0, spectrographCanvas.width, spectrographCanvas.height);
            ctx.fillStyle = '#000';
            ctx.fillRect(0, 0, spectrographCanvas.width, spectrographCanvas.height);
            detectedNoteSpan.textContent = 'N/A';

            // Disable relevant buttons
            startRecordingBtn.disabled = true;
            stopRecordingBtn.disabled = true;
            stopAllAudioBtn.disabled = true;
            statusMessage.textContent = 'Ready for new input.';
        }

        // Function to load and play audio from file
        async function loadAndPlayAudio(file) {
            stopAllSources();
            initAudioContext();

            statusMessage.textContent = 'Loading audio file...';

            try {
                const arrayBuffer = await file.arrayBuffer();
                const audioBuffer = await audioContext.decodeAudioData(arrayBuffer);

                fileSource = audioContext.createBufferSource();
                fileSource.buffer = audioBuffer;

                fileSource.connect(analyser);
                analyser.connect(audioContext.destination);

                fileSource.loop = true;
                fileSource.start(0);

                statusMessage.textContent = `Playing from file: ${file.name}`;
                updateSpectrograph();
                startRecordingBtn.disabled = false;
                stopAllAudioBtn.disabled = false;
            } catch (error) {
                console.error('Error loading or playing audio:', error);
                statusMessage.textContent = 'Error loading audio file.';
                showMessageBox('Failed to load audio file. Please try another file.');
                startRecordingBtn.disabled = true;
                stopAllAudioBtn.disabled = true;
            }
        }

        // Function to start microphone input
        async function startMicrophone() {
            stopAllSources();
            initAudioContext();

            statusMessage.textContent = 'Requesting microphone access...';

            try {
                mediaStream = await navigator.mediaDevices.getUserMedia({ audio: true });
                micSource = audioContext.createMediaStreamSource(mediaStream);

                micSource.connect(analyser);
                analyser.connect(audioContext.destination);

                statusMessage.textContent = 'Recording from microphone...';
                updateSpectrograph();
                startRecordingBtn.disabled = false;
                stopAllAudioBtn.disabled = false;
            } catch (error) {
                console.error('Error accessing microphone:', error);
                statusMessage.textContent = 'Microphone access denied or no microphone found.';
                showMessageBox('Could not access microphone. Please ensure it is connected and permissions are granted.');
                startRecordingBtn.disabled = true;
                stopAllAudioBtn.disabled = true;
            }
        }

        // Function to start recording
        function startRecording() {
            if (!audioContext || (!fileSource && !micSource)) {
                showMessageBox('Please load an audio file or start microphone input first.');
                return;
            }

            recordedChunks = [];
            isRecording = true;
            startRecordingBtn.disabled = true;
            stopRecordingBtn.disabled = false;
            startRecordingBtn.classList.add('recording');
            statusMessage.textContent = 'Recording audio...';

            let streamToRecord;
            if (micSource) {
                streamToRecord = mediaStream;
            } else if (fileSource) {
                const destination = audioContext.createMediaStreamDestination();
                analyser.connect(destination);
                streamToRecord = destination.stream;
            } else {
                showMessageBox('No active audio source to record.');
                isRecording = false;
                startRecordingBtn.disabled = false;
                stopRecordingBtn.disabled = true;
                startRecordingBtn.classList.remove('recording');
                return;
            }

            try {
                mediaRecorder = new MediaRecorder(streamToRecord);

                mediaRecorder.ondataavailable = (event) => {
                    if (event.data.size > 0) {
                        recordedChunks.push(event.data);
                    }
                };

                mediaRecorder.onstop = () => {
                    const blob = new Blob(recordedChunks, { type: 'audio/webm' });
                    const url = URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.style.display = 'none';
                    a.href = url;
                    a.download = 'spectrograph_recording.webm';
                    document.body.appendChild(a);
                    a.click();
                    window.URL.revokeObjectURL(url);

                    isRecording = false;
                    startRecordingBtn.disabled = false;
                    stopRecordingBtn.disabled = true;
                    startRecordingBtn.classList.remove('recording');
                    statusMessage.textContent = 'Recording saved. Ready for new input.';

                    if (fileSource) {
                        analyser.disconnect(streamToRecord);
                        analyser.connect(audioContext.destination);
                    }
                };

                mediaRecorder.start();
                statusMessage.textContent = 'Recording... (Click Stop Recording to save)';
            } catch (e) {
                console.error('Error starting MediaRecorder:', e);
                showMessageBox('Failed to start recording. Your browser might not support MediaRecorder or there\'s an issue with the audio stream.');
                isRecording = false;
                startRecordingBtn.disabled = false;
                stopRecordingBtn.disabled = true;
                startRecordingBtn.classList.remove('recording');
            }
        }

        // Function to stop recording
        function stopRecording() {
            if (mediaRecorder && mediaRecorder.state !== 'inactive') {
                mediaRecorder.stop();
            }
        }

        // Function to save the current spectrogram image
        function saveSpectrogramImage() {
            if (!spectrographCanvas || spectrographCanvas.width === 0 || spectrographCanvas.height === 0) {
                showMessageBox('No spectrogram data to save. Please play audio first.');
                return;
            }

            const finalCanvas = document.createElement('canvas');
            finalCanvas.width = spectrographCanvas.width;
            finalCanvas.height = spectrographCanvas.height;
            const finalCtx = finalCanvas.getContext('2d');

            finalCtx.drawImage(spectrographCanvas, 0, 0);

            const minFreq = parseFloat(minFreqSlider.value);
            const maxFreq = parseFloat(maxFreqSlider.value);
            const freqRangeHeight = maxFreq - minFreq;
            const pixelsPerHz = finalCanvas.height / freqRangeHeight;

            const tickFrequencies = [
                50, 100, 200, 300, 400, 500, 600, 700, 800, 900,
                1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000,
                10000, 12000, 14000, 16000, 18000, 20000
            ];

            finalCtx.font = '12px Inter';
            finalCtx.fillStyle = '#a0aec0';
            finalCtx.strokeStyle = 'rgba(160, 174, 192, 0.3)';
            finalCtx.lineWidth = 0.5;

            tickFrequencies.forEach(freq => {
                if (freq >= minFreq && freq <= maxFreq) {
                    const y_pos = finalCanvas.height - ((freq - minFreq) * pixelsPerHz);

                    if (y_pos >= 0 && y_pos <= finalCanvas.height) {
                        finalCtx.beginPath();
                        finalCtx.moveTo(0, y_pos);
                        finalCtx.lineTo(finalCanvas.width, y_pos);
                        finalCtx.stroke();

                        let label = freq + ' Hz';
                        if (freq >= 1000) {
                            label = (freq / 1000) + ' kHz';
                        }
                        finalCtx.textAlign = 'left';
                        finalCtx.fillText(label, 5, y_pos - 2);
                    }
                }
            });

            const imageURI = finalCanvas.toDataURL('image/png');
            const a = document.createElement('a');
            a.href = imageURI;
            a.download = 'spectrogram_with_grid.png';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            showMessageBox('Spectrogram image with frequency grid saved as spectrogram_with_grid.png');
        }

        // Function to update spectrograph visualization
        function updateSpectrograph() {
            if (!analyser) return;

            const bufferLength = analyser.frequencyBinCount;
            const dataArray = new Uint8Array(bufferLength);
            analyser.getByteFrequencyData(dataArray);

            const tempCanvas = document.createElement('canvas');
            tempCanvas.width = spectrographCanvas.width;
            tempCanvas.height = spectrographCanvas.height;
            const tempCtx = tempCanvas.getContext('2d');

            tempCtx.drawImage(spectrographCanvas, barWidth, 0, spectrographCanvas.width - barWidth, spectrographCanvas.height, 0, 0, spectrographCanvas.width - barWidth, spectrographCanvas.height);

            ctx.clearRect(0, 0, spectrographCanvas.width, spectrographCanvas.height);
            ctx.fillStyle = '#000';
            ctx.fillRect(0, 0, spectrographCanvas.width, spectrographCanvas.height);
            ctx.drawImage(tempCanvas, 0, 0);

            const minFreq = parseFloat(minFreqSlider.value);
            const maxFreq = parseFloat(maxFreqSlider.value);

            minFreqNumberInput.value = minFreq;
            maxFreqNumberInput.value = maxFreq;
            minFreqValueSpan.textContent = `${minFreq} Hz`;
            maxFreqValueSpan.textContent = `${maxFreq} Hz`;

            const frequencyResolution = audioContext.sampleRate / analyser.fftSize;

            const minBin = Math.floor(minFreq / frequencyResolution);
            const maxBin = Math.ceil(maxFreq / frequencyResolution);

            const effectiveMinBin = Math.max(0, Math.min(minBin, bufferLength - 1));
            const effectiveMaxBin = Math.min(bufferLength - 1, Math.max(maxBin, effectiveMinBin));

            const visibleBins = effectiveMaxBin - effectiveMinBin + 1;

            if (visibleBins <= 0) {
                ctx.fillStyle = '#e2e8f0';
                ctx.font = '16px Inter';
                ctx.textAlign = 'center';
                ctx.fillText('Adjust frequency range to see data', spectrographCanvas.width / 2, spectrographCanvas.height / 2);
                detectedNoteSpan.textContent = 'N/A';
                animationFrameId = requestAnimationFrame(updateSpectrograph);
                return;
            }

            const freqRangeHeight = maxFreq - minFreq;
            const pixelsPerHz = spectrographCanvas.height / freqRangeHeight;

            const x_pos = spectrographCanvas.width - barWidth;

            let dominantFrequency = 0;
            let maxMagnitude = 0;

            for (let i = effectiveMinBin; i <= effectiveMaxBin; i++) {
                const freq = i * frequencyResolution;
                const magnitude = dataArray[i];

                if (magnitude > maxMagnitude) {
                    maxMagnitude = magnitude;
                    dominantFrequency = freq;
                }

                let r = Math.floor(magnitude * 1);
                let g = Math.floor(magnitude * 0.5);
                let b = Math.floor(magnitude * 0.2);
                ctx.fillStyle = `rgb(${r}, ${g}, ${b})`;

                const y_start = spectrographCanvas.height - ((freq - minFreq) * pixelsPerHz);
                const y_end = spectrographCanvas.height - (((freq + frequencyResolution) - minFreq) * pixelsPerHz);

                const drawY = Math.min(y_start, y_end);
                const drawHeight = Math.abs(y_start - y_end);

                if (drawY + drawHeight > 0 && drawY < spectrographCanvas.height) {
                   ctx.fillRect(x_pos, drawY, barWidth, drawHeight);
                }
            }

            // --- Draw Frequency Grid Overlay ---
            const tickFrequencies = [
                50, 100, 200, 300, 400, 500, 600, 700, 800, 900,
                1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000,
                10000, 12000, 14000, 16000, 18000, 20000
            ];

            ctx.font = '12px Inter';
            ctx.fillStyle = '#a0aec0';
            ctx.strokeStyle = 'rgba(160, 174, 192, 0.3)';
            ctx.lineWidth = 0.5;

            tickFrequencies.forEach(freq => {
                if (freq >= minFreq && freq <= maxFreq) {
                    const y_pos = spectrographCanvas.height - ((freq - minFreq) * pixelsPerHz);

                    if (y_pos >= 0 && y_pos <= spectrographCanvas.height) {
                        ctx.beginPath();
                        ctx.moveTo(0, y_pos);
                        ctx.lineTo(spectrographCanvas.width, y_pos);
                        ctx.stroke();

                        let label = freq + ' Hz';
                        if (freq >= 1000) {
                            label = (freq / 1000) + ' kHz';
                        }
                        ctx.textAlign = 'left';
                        ctx.fillText(label, 5, y_pos - 2);
                    }
                }
            });
            // --- End Draw Frequency Grid Overlay ---

            // --- Display Detected Note ---
            if (dominantFrequency > 0 && maxMagnitude > 0) {
                const detectedNote = getNoteFromFrequency(dominantFrequency);
                detectedNoteSpan.textContent = `${detectedNote} (${dominantFrequency.toFixed(2)} Hz)`;

                const dominantFreqY = spectrographCanvas.height - ((dominantFrequency - minFreq) * pixelsPerHz);
                if (dominantFreqY >= 0 && dominantFreqY <= spectrographCanvas.height) {
                    ctx.strokeStyle = dominantFreqLineColor; // Use configurable color
                    ctx.lineWidth = dominantFreqLineWidth; // Use configurable width
                    ctx.beginPath();
                    ctx.moveTo(0, dominantFreqY);
                    ctx.lineTo(spectrographCanvas.width, dominantFreqY);
                    ctx.stroke();

                    ctx.fillStyle = dominantFreqLabelColor; // Use configurable color
                    ctx.font = dominantFreqLabelFont; // Use configurable font
                    ctx.textAlign = 'right';
                    ctx.fillText(`${detectedNote}`, spectrographCanvas.width + dominantFreqLabelOffsetX, dominantFreqY + dominantFreqLabelOffsetY); // Use configurable offsets
                }
            } else {
                detectedNoteSpan.textContent = 'N/A';
            }
            // --- End Display Detected Note ---

            animationFrameId = requestAnimationFrame(updateSpectrograph);
        }

        // Event listener for audio file input
        audioFile.addEventListener('change', (event) => {
            const file = event.target.files[0];
            if (file) {
                loadAndPlayAudio(file);
            } else {
                statusMessage.textContent = 'No audio file selected.';
                startRecordingBtn.disabled = true;
                stopAllAudioBtn.disabled = true;
                detectedNoteSpan.textContent = 'N/A';
            }
        });

        // Event listener for microphone button
        startMicrophoneBtn.addEventListener('click', () => {
            startMicrophone();
        });

        // Event listeners for recording buttons
        startRecordingBtn.addEventListener('click', startRecording);
        stopRecordingBtn.addEventListener('click', stopRecording);

        // Event listener for saving spectrogram image
        saveSpectrogramBtn.addEventListener('click', saveSpectrogramImage);

        // Event listener for stop all audio button
        stopAllAudioBtn.addEventListener('click', stopAllSources);

        // Event listener for A4=432Hz button
        setA432HzBtn.addEventListener('click', () => {
            const newMinFreq = 400; // Example range around 432 Hz
            const newMaxFreq = 500;

            minFreqSlider.value = newMinFreq;
            maxFreqSlider.value = newMaxFreq;
            minFreqNumberInput.value = newMinFreq;
            maxFreqNumberInput.value = newMaxFreq;

            minFreqValueSpan.textContent = `${newMinFreq} Hz`;
            maxFreqValueSpan.textContent = `${newMaxFreq} Hz`;
        });

        // Event listeners for frequency range sliders
        minFreqSlider.addEventListener('input', () => {
            let newMin = parseFloat(minFreqSlider.value);
            let currentMax = parseFloat(maxFreqSlider.value);
            if (newMin >= currentMax) {
                newMin = currentMax - 10;
                minFreqSlider.value = newMin;
            }
            minFreqNumberInput.value = newMin;
            minFreqValueSpan.textContent = `${newMin} Hz`;
        });

        maxFreqSlider.addEventListener('input', () => {
            let newMax = parseFloat(maxFreqSlider.value);
            let currentMin = parseFloat(minFreqSlider.value);
            if (newMax <= currentMin) {
                newMax = currentMin + 10;
                maxFreqSlider.value = newMax;
            }
            maxFreqNumberInput.value = newMax;
            maxFreqValueSpan.textContent = `${newMax} Hz`;
        });

        // Event listeners for number inputs
        minFreqNumberInput.addEventListener('change', () => {
            let newMin = parseFloat(minFreqNumberInput.value);
            let currentMax = parseFloat(maxFreqNumberInput.value);
            const minAllowed = parseFloat(minFreqNumberInput.min);
            const maxAllowed = parseFloat(minFreqNumberInput.max);

            if (isNaN(newMin) || newMin < minAllowed) {
                newMin = minAllowed;
            } else if (newMin >= currentMax) {
                newMin = currentMax - 10;
            } else if (newMin > maxAllowed) {
                newMin = maxAllowed;
            }
            minFreqNumberInput.value = newMin;
            minFreqSlider.value = newMin;
            minFreqValueSpan.textContent = `${newMin} Hz`;
        });

        maxFreqNumberInput.addEventListener('change', () => {
            let newMax = parseFloat(maxFreqNumberInput.value);
            let currentMin = parseFloat(minFreqNumberInput.value);
            const minAllowed = parseFloat(maxFreqNumberInput.min);
            const maxAllowed = parseFloat(maxFreqNumberInput.max);

            if (isNaN(newMax) || newMax > maxAllowed) {
                newMax = maxAllowed;
            } else if (newMax <= currentMin) {
                newMax = currentMin + 10;
            } else if (newMax < minAllowed) {
                newMax = minAllowed;
            }
            maxFreqNumberInput.value = newMax;
            maxFreqSlider.value = newMax;
            maxFreqValueSpan.textContent = `${newMax} Hz`;
        });


        // Initial setup for canvas size
        function resizeCanvas() {
            spectrographCanvas.width = spectrographCanvas.offsetWidth;
            spectrographCanvas.height = spectrographCanvas.offsetHeight;
        }

        // Call resizeCanvas initially and on window resize
        window.addEventListener('resize', resizeCanvas);
        resizeCanvas(); // Initial call

        // Disable buttons initially
        startRecordingBtn.disabled = true;
        stopRecordingBtn.disabled = true;
        stopAllAudioBtn.disabled = true;

        // Stop animation and audio when page is closed or navigation occurs
        window.addEventListener('beforeunload', () => {
            stopAllSources();
            if (analyser) {
                analyser.disconnect();
            }
            if (audioContext) {
                audioContext.close();
            }
        });
    </script>
</body>
</html>
