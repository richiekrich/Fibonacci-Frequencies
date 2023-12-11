import tkinter as tk
from PIL import Image, ImageTk
from threading import Thread, Event
import simpleaudio as sa
import numpy as np
from scipy import signal

class AnimatedGIFLabel(tk.Label):
    def __init__(self, master, gif_path, delay=100):
        im = Image.open(gif_path)
        seq = []
        try:
            while True:
                seq.append(im.copy())
                im.seek(len(seq))  # Skip to next frame
        except EOFError:
            pass

        self.frames = [ImageTk.PhotoImage(image) for image in seq]
        self.delay = delay
        self.current = 0
        super().__init__(master, image=self.frames[0])

        self.after(self.delay, self.next_frame)

    def next_frame(self):
        self.current = (self.current + 1) % len(self.frames)
        self.configure(image=self.frames[self.current])
        self.after(self.delay, self.next_frame)

def create_gif_label(master, gif_path):
    # Create and return the AnimatedGIFLabel
    return AnimatedGIFLabel(master, gif_path)



def play_frequency(frequency, duration, volume=1.0, sample_rate=44100, attack_duration=0.01):
    # Generate time array
    t = np.linspace(0, duration, int(duration * sample_rate), False)
    
    # Generate sine wave
    note = np.sin(frequency * t * 2 * np.pi)

    # Create attack envelope
    attack_samples = int(sample_rate * attack_duration)
    attack_envelope = np.linspace(0, 1, attack_samples)**2  # Exponential ramp

    # Apply envelope to the note
    note[:attack_samples] *= attack_envelope

    # Scale to the appropriate volume
    audio = note * (2**15 - 1) * volume / np.max(np.abs(note))
    return audio.astype(np.int16)


def apply_low_pass_filter(audio, cutoff):
    nyquist = 0.5 * 44100  # Nyquist frequency
    normal_cutoff = cutoff / nyquist
    b, a = signal.butter(4, normal_cutoff, btype='low', analog=False)
    filtered_audio = signal.lfilter(b, a, audio)
    return filtered_audio.astype(np.int16)
    
    # Convert audio to floating-point for processing
    audio_float = audio.astype(np.float32) / (2**15 - 1)
    
 
    
def play_arpeggio(frequencies, bpm, stop_event, volume, cutoff, repetitions=10, sample_rate=44100):
    # Calculate note duration based on BPM
    note_duration = 60 / bpm

    # Create a buffer to hold the entire sequence for all repetitions
    full_sequence_buffer = []

    for frequency in frequencies:
        # Generate the note
        note = play_frequency(frequency, note_duration, volume, sample_rate)
        # Apply low-pass filter
        filtered_note = apply_low_pass_filter(note, cutoff)
        # Append to the sequence buffer
        full_sequence_buffer.extend(filtered_note)

    # Repeat the full sequence for the desired number of repetitions
    repeated_sequence = np.tile(full_sequence_buffer, repetitions)

    # Convert the buffer to a numpy array
    repeated_sequence_audio = np.array(repeated_sequence).astype(np.int16)

    # Play the audio sequence
    play_obj = sa.play_buffer(repeated_sequence_audio, 1, 2, sample_rate)
    while not stop_event.is_set():
        if play_obj.is_playing():
            continue
        play_obj = sa.play_buffer(repeated_sequence_audio, 1, 2, sample_rate)

    play_obj.stop()


# Function to start GIF animation in a new thread
def start_gif_animation():
    display_gif_thread = Thread(target=display_gif)
    display_gif_thread.start()

# Frequencies to be played
fibonacci_frequencies = [34, 55, 89, 144, 233, 377, 610, 987, 1597, 2584, 4181, 6765, 10946, 17711]

# Event to stop the playback thread
stop_event = Event()

# Function to start playing audio in a new thread
def start_playing():
    global stop_event  # Use the global stop_event variable
    stop_event.clear()
    # Only include the necessary arguments in the play_arpeggio function call
    play_thread = Thread(target=play_arpeggio, args=(fibonacci_frequencies, bpm_scale.get(), stop_event, volume_scale.get(), cutoff_scale.get()))
    play_thread.start()


def stop_playing():
    global stop_event  # Use the global stop_event variable
    stop_event.set()

# Creating a Tkinter window
root = tk.Tk()
root.title("Fibonacci Arpeggio Player")

# Volume Slider
volume_scale = tk.Scale(root, from_=0, to=1, resolution=0.01, orient='horizontal', label='Volume')
volume_scale.set(0.5)
volume_scale.pack()

# BPM Slider
bpm_scale = tk.Scale(root, from_=30, to=500, orient='horizontal', label='BPM')
bpm_scale.set(60)  # Default BPM
bpm_scale.pack()

# Low-Pass Filter Cutoff Slider
cutoff_scale = tk.Scale(root, from_=0, to=5000, orient='horizontal', label='Low-Pass Cutoff')
cutoff_scale.set(1000)  # Default cutoff frequency
cutoff_scale.pack()

# Play button
play_button = tk.Button(root, text='Play', command=start_playing)  # This will trigger the start_playing function
play_button.pack()

# Stop button
stop_button = tk.Button(root, text='Stop', command=stop_playing)
stop_button.pack()

# Create and add the animated GIF label to the Tkinter window
gif_path = r'C:\Scripts\Fib.gif'  # Replace with your GIF's actual path
label = create_gif_label(root, gif_path)
label.pack()

# Run the main application loop
root.mainloop()

# Run the main application loop
root.mainloop()
