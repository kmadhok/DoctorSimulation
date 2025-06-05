// Audio Manager Module - Handles all audio-related functionality
export class AudioManager {
    constructor() {
        this.audioContext = null;
        this.currentAudioSource = null;
        this.isInitialized = false;
    }

    async initializeAudioContext() {
        if (this.audioContext && this.audioContext.state === 'running') {
            return true;
        }

        try {
            this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
            console.log('AudioContext initialized with state:', this.audioContext.state);
            
            if (this.audioContext.state === 'suspended') {
                await this.audioContext.resume();
                console.log('AudioContext resumed, new state:', this.audioContext.state);
            }
            
            this.isInitialized = true;
            return true;
        } catch (error) {
            console.error('Error initializing AudioContext:', error);
            return false;
        }
    }

    stopCurrentAudio() {
        if (this.currentAudioSource) {
            console.log('Stopping current audio source');
            this.currentAudioSource.stop();
            if (this.currentAudioSource.onended) {
                this.currentAudioSource.onended = null;
            }
            this.currentAudioSource = null;
        }
    }

    async playAudioResponse(base64Audio) {
        if (!base64Audio || base64Audio.length === 0) {
            console.error('Empty audio data received');
            return false;
        }

        // Ensure AudioContext is initialized
        if (!this.isInitialized) {
            const initialized = await this.initializeAudioContext();
            if (!initialized) {
                return this.playWithHtmlAudio(base64Audio);
            }
        }

        // Stop any currently playing audio
        this.stopCurrentAudio();

        try {
            // Convert base64 to ArrayBuffer
            const binaryString = atob(base64Audio);
            const len = binaryString.length;
            const bytes = new Uint8Array(len);
            
            for (let i = 0; i < len; i++) {
                bytes[i] = binaryString.charCodeAt(i);
            }

            // Decode audio data
            let audioBuffer;
            try {
                audioBuffer = await this.audioContext.decodeAudioData(bytes.buffer);
                console.log(`Audio decoded successfully, duration: ${audioBuffer.duration}s`);
            } catch (decodeError) {
                console.error('Failed to decode audio:', decodeError);
                return this.playWithHtmlAudio(base64Audio);
            }

            // Create and play audio source
            const source = this.audioContext.createBufferSource();
            source.buffer = audioBuffer;
            source.connect(this.audioContext.destination);

            this.currentAudioSource = source;

            source.onended = () => {
                console.log('Audio playback completed');
                this.currentAudioSource = null;
            };

            source.start(0);
            console.log('Audio playback started');
            return true;

        } catch (error) {
            console.error('Error playing audio:', error);
            return this.playWithHtmlAudio(base64Audio);
        }
    }

    playWithHtmlAudio(base64Audio) {
        try {
            console.log('Using HTML5 Audio fallback');
            const audioElement = new Audio(`data:audio/mp3;base64,${base64Audio}`);
            audioElement.play().then(() => {
                console.log('HTML5 Audio playback successful');
            }).catch(htmlAudioError => {
                console.error('HTML5 Audio playback failed:', htmlAudioError);
            });
            return true;
        } catch (error) {
            console.error('HTML5 Audio fallback failed:', error);
            return false;
        }
    }

    float32ToWav(float32, sampleRate = 16000) {
        const buffer = new ArrayBuffer(44 + float32.length * 2);
        const view = new DataView(buffer);

        // RIFF header
        const writeString = (offset, str) =>
            str.split('').forEach((s, i) => view.setUint8(offset + i, s.charCodeAt(0)));

        writeString(0, 'RIFF');
        view.setUint32(4, 36 + float32.length * 2, true);
        writeString(8, 'WAVE');
        writeString(12, 'fmt ');
        view.setUint32(16, 16, true);   // Sub-chunk size
        view.setUint16(20, 1, true);    // PCM
        view.setUint16(22, 1, true);    // Mono
        view.setUint32(24, sampleRate, true);
        view.setUint32(28, sampleRate * 2, true); // Byte rate
        view.setUint16(32, 2, true);    // Block align
        view.setUint16(34, 16, true);   // Bits per sample
        writeString(36, 'data');
        view.setUint32(40, float32.length * 2, true);

        // PCM samples
        for (let i = 0; i < float32.length; i++) {
            const s = Math.max(-1, Math.min(1, float32[i]));
            view.setInt16(44 + i * 2, s < 0 ? s * 0x8000 : s * 0x7FFF, true);
        }
        
        return new Blob([view], { type: "audio/wav" });
    }

    async testMicrophoneAccess() {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            stream.getTracks().forEach(track => track.stop());
            return true;
        } catch (error) {
            console.error('Microphone access error:', error);
            return false;
        }
    }
} 