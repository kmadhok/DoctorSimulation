// Mock the MediaRecorder and related APIs
const mockMediaRecorder = {
    start: jest.fn(),
    stop: jest.fn(),
    stream: {
        getTracks: () => [{
            stop: jest.fn()
        }]
    },
    ondataavailable: null,
    onstop: null
};

const mockAudioContext = {
    createBufferSource: jest.fn().mockReturnValue({
        connect: jest.fn(),
        start: jest.fn(),
        stop: jest.fn()
    }),
    decodeAudioData: jest.fn().mockResolvedValue(new ArrayBuffer(0))
};

// Mock the global objects
global.MediaRecorder = jest.fn().mockImplementation(() => mockMediaRecorder);
global.AudioContext = jest.fn().mockImplementation(() => mockAudioContext);
global.webkitAudioContext = jest.fn().mockImplementation(() => mockAudioContext);

// Mock the navigator.mediaDevices
global.navigator.mediaDevices = {
    getUserMedia: jest.fn().mockResolvedValue({
        getTracks: () => [{
            stop: jest.fn()
        }]
    })
};

// Mock fetch
global.fetch = jest.fn();

// Mock DOM elements
document.body.innerHTML = `
    <button id="recordButton"></button>
    <div id="status"></div>
    <div id="conversation"></div>
    <select id="simulationSelect"></select>
`;

// Import the main.js file
require('../static/js/main.js');

describe('Audio Recording Tests', () => {
    beforeEach(() => {
        // Clear all mocks before each test
        jest.clearAllMocks();
        
        // Reset DOM elements
        document.getElementById('status').textContent = '';
        document.getElementById('conversation').innerHTML = '';
        document.getElementById('recordButton').className = '';
    });

    test('should initialize audio recording on button press', async () => {
        const recordButton = document.getElementById('recordButton');
        
        // Simulate mousedown event
        recordButton.dispatchEvent(new MouseEvent('mousedown'));
        
        // Check if MediaRecorder was initialized
        expect(MediaRecorder).toHaveBeenCalled();
        expect(mockMediaRecorder.start).toHaveBeenCalled();
        expect(document.getElementById('status').textContent).toBe('Recording...');
        expect(recordButton.classList.contains('recording')).toBe(true);
    });

    test('should stop recording on button release', async () => {
        const recordButton = document.getElementById('recordButton');
        
        // Start recording
        recordButton.dispatchEvent(new MouseEvent('mousedown'));
        
        // Stop recording
        recordButton.dispatchEvent(new MouseEvent('mouseup'));
        
        // Check if recording was stopped
        expect(mockMediaRecorder.stop).toHaveBeenCalled();
        expect(document.getElementById('status').textContent).toBe('Processing...');
        expect(recordButton.classList.contains('recording')).toBe(false);
    });

    test('should handle recording errors gracefully', async () => {
        // Mock getUserMedia to reject
        navigator.mediaDevices.getUserMedia.mockRejectedValueOnce(new Error('Permission denied'));
        
        const recordButton = document.getElementById('recordButton');
        
        // Try to start recording
        recordButton.dispatchEvent(new MouseEvent('mousedown'));
        
        // Check error handling
        expect(document.getElementById('status').textContent).toContain('Error');
    });

    test('should process audio data after recording', async () => {
        // Mock successful fetch response
        global.fetch.mockResolvedValueOnce({
            json: () => Promise.resolve({
                status: 'success',
                user_transcription: 'Test transcription',
                assistant_response_text: 'Test response',
                assistant_response_audio: 'base64_audio_data'
            })
        });

        const recordButton = document.getElementById('recordButton');
        
        // Start and stop recording
        recordButton.dispatchEvent(new MouseEvent('mousedown'));
        recordButton.dispatchEvent(new MouseEvent('mouseup'));
        
        // Simulate ondataavailable event
        const audioData = new Blob(['test'], { type: 'audio/wav' });
        mockMediaRecorder.ondataavailable({ data: audioData });
        
        // Simulate onstop event
        mockMediaRecorder.onstop();
        
        // Wait for async operations
        await new Promise(resolve => setTimeout(resolve, 0));
        
        // Check if audio was processed
        expect(fetch).toHaveBeenCalledWith('/process_audio', expect.any(Object));
        expect(document.getElementById('conversation').children.length).toBe(2); // User and assistant messages
    });

    test('should handle processing errors gracefully', async () => {
        // Mock failed fetch response
        global.fetch.mockRejectedValueOnce(new Error('Network error'));
        
        const recordButton = document.getElementById('recordButton');
        
        // Start and stop recording
        recordButton.dispatchEvent(new MouseEvent('mousedown'));
        recordButton.dispatchEvent(new MouseEvent('mouseup'));
        
        // Simulate ondataavailable event
        const audioData = new Blob(['test'], { type: 'audio/wav' });
        mockMediaRecorder.ondataavailable({ data: audioData });
        
        // Simulate onstop event
        mockMediaRecorder.onstop();
        
        // Wait for async operations
        await new Promise(resolve => setTimeout(resolve, 0));
        
        // Check error handling
        expect(document.getElementById('status').textContent).toContain('Error');
    });

    test('should stop TTS playback and start recording when hold-to-speak is pressed during playback', async () => {
        // Mock successful fetch response with audio
        global.fetch.mockResolvedValueOnce({
            json: () => Promise.resolve({
                status: 'success',
                user_transcription: 'Test transcription',
                assistant_response_text: 'Test response',
                assistant_response_audio: 'base64_audio_data'
            })
        });

        const recordButton = document.getElementById('recordButton');
        
        // First, simulate a complete recording cycle to get TTS playing
        recordButton.dispatchEvent(new MouseEvent('mousedown'));
        recordButton.dispatchEvent(new MouseEvent('mouseup'));
        
        // Simulate ondataavailable event
        const audioData = new Blob(['test'], { type: 'audio/wav' });
        mockMediaRecorder.ondataavailable({ data: audioData });
        
        // Simulate onstop event
        mockMediaRecorder.onstop();
        
        // Wait for async operations
        await new Promise(resolve => setTimeout(resolve, 0));
        
        // Verify that audio context was created and source was started
        expect(AudioContext).toHaveBeenCalled();
        const audioSource = mockAudioContext.createBufferSource();
        expect(audioSource.start).toHaveBeenCalled();
        
        // Now simulate pressing hold-to-speak during TTS playback
        recordButton.dispatchEvent(new MouseEvent('mousedown'));
        
        // Verify that the current audio source was stopped
        expect(audioSource.stop).toHaveBeenCalled();
        
        // Verify that new recording started
        expect(MediaRecorder).toHaveBeenCalled();
        expect(mockMediaRecorder.start).toHaveBeenCalled();
        expect(document.getElementById('status').textContent).toBe('Recording...');
        expect(recordButton.classList.contains('recording')).toBe(true);
        
        // Verify that the audio tracks from the previous recording were stopped
        expect(mockMediaRecorder.stream.getTracks()[0].stop).toHaveBeenCalled();
    });

    test('should handle multiple rapid hold-to-speak presses correctly', async () => {
        const recordButton = document.getElementById('recordButton');
        
        // First press
        recordButton.dispatchEvent(new MouseEvent('mousedown'));
        expect(mockMediaRecorder.start).toHaveBeenCalledTimes(1);
        
        // Release
        recordButton.dispatchEvent(new MouseEvent('mouseup'));
        expect(mockMediaRecorder.stop).toHaveBeenCalledTimes(1);
        
        // Second press immediately after
        recordButton.dispatchEvent(new MouseEvent('mousedown'));
        expect(mockMediaRecorder.start).toHaveBeenCalledTimes(2);
        
        // Verify that the status is correct
        expect(document.getElementById('status').textContent).toBe('Recording...');
        expect(recordButton.classList.contains('recording')).toBe(true);
        
        // Verify that the previous audio tracks were properly cleaned up
        expect(mockMediaRecorder.stream.getTracks()[0].stop).toHaveBeenCalled();
    });
}); 