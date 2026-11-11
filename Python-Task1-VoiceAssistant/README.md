Python Voice Assistant 🎙️

A simple voice-controlled assistant built with Python. It listens to voice commands, converts speech into text, performs basic tasks, and responds using text-to-speech.

🌟 Features – Beginner Tier

The project currently includes the following features:

- Voice Recognition: Listens to the user's voice through the microphone and converts speech into text.
- Text-to-Speech: Responds verbally using the "pyttsx3" library.
- Greeting: Responds to basic greetings such as "Hello" and "Hi".
- Tell the Time: Announces the current time.
- Tell the Date: Announces today's date.
- Web Search: Opens Google search results in the default web browser based on the user's voice command.
- Exit Command: Stops the assistant when the user says "Goodbye", "Exit", or "Stop".

🛠️ Technologies Used

- Python – Main programming language.
- SpeechRecognition – Converts spoken commands into text.
- PyAudio – Provides microphone input for speech recognition.
- pyttsx3 – Converts text responses into speech.
- datetime – Retrieves the current date and time.
- webbrowser – Opens Google search results in the default browser.
- urllib.parse – Encodes search queries for URLs.

⚙️ Installation

1. Clone the repository:
   
   git clone <your-repository-url>

2. Navigate to the project directory:
   
   cd <project-folder>

3. Install the required libraries:
   
   pip install "SpeechRecognition[audio]" pyttsx3

▶️ How to Run

Run the Python file:

python main.py

Make sure your microphone is connected and accessible.

🗣️ Available Voice Commands

Voice Command| Action
Hello / Hi| Greets the user
What time is it?| Announces the current time
What is today's date?| Announces today's date
Search for Python tutorials| Opens Google search results
Goodbye / Exit / Stop| Closes the assistant

📌 Notes

- An active internet connection is required for Google speech recognition and web searches.
- A working microphone is required to provide voice commands.
- The assistant uses the system's available text-to-speech voices.

🚀 Project Status

Beginner Tier – Completed

This version focuses on basic voice interaction, speech recognition, text-to-speech, and simple command handling. More advanced features may be added in future versions.
