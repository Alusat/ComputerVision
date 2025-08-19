***HandTracking Module***

This module provides real-time hand tracking and detection using Mediapipe.

***Files***
- `HandTrackingMin.py`: Minimal example to run hand tracking.
- `HandTrackingModule.py`: Core classes and functions for hand detection.
- `RPS-ineitor.py`: A small Rock-Paper-Scissors game that uses hand detection to determine
  the winner and displays the corresponding image from the `images/` folder.
- `images/`: Contains images used by RPS-ineitor.py.
- `__pycache__/`: Python cache files.

***RPS-ineitor.py Controls***
- Press **'q'** to quit the program.
- Press **'i'** to show additional debug information.

***Troubleshooting***
- Ensure your webcam is working.
- Make sure desktop apps have permission to access the camera and it is not blocked by antivirus.
- Verify that no other application is using the camera.
- Make sure dependencies are installed and that Python 3.10-3.11 is being used for Mediapipe compatibility.
- Windows users: If you are running this from the Windows Subsystem for Linux (WSL), it may work better
  to run the program directly from Windows PowerShell instead.


