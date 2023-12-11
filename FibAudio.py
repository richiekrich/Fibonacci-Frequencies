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
