# DeepFake Detection Projects
This repository contains two projects aimed at detecting DeepFake images and videos using Convolutional Neural Network (CNN) sequential models.

# Chrome Extension
The Chrome extension integrated with a CNN sequential model trained on image datasets achieves an accuracy of approximately 93%. The frontend of the extension is developed using HTML, CSS, and JavaScript and deployed using Flask.

## Usage
1. Clone the repository:
   ```
   git clone https://github.com/gilhotraapoorva/DeepFake_MultiFace_Videos.git
2. Run the server using the command:
   ```
   python3 app.py
   ```

3. Start the extension by clicking on "Capture Screen". Share any screen containing images, and the extension will capture the screen and display the result indicating whether the image is real or a deepfake.


# Full Stack DeepFake Detection Project

This repository contains a full-stack project deployed using Flask and integrated with a Convolutional Neural Network (CNN) sequential model. The project focuses on deepfake detection in video datasets, particularly addressing scenarios where videos contain multiple persons.

## Project Overview

Deepfake technology has raised concerns regarding its potential misuse, particularly in creating fabricated content involving individuals. This project aims to tackle such issues by providing a solution capable of detecting deepfake videos, even in cases where multiple persons are involved.

The application has practical implications, such as combating deepfake pornography and aiding law enforcement in identifying potential instances of deepfake manipulation, for example, in cases of child abduction where kidnappers might fabricate videos to mislead investigations.

## Features
* Deepfake detection in videos with multiple persons.
* Frontend developed using HTML, CSS, and JavaScript.
* Deployment through Flask.
* Integration with a CNN sequential model.

## Usage
To use this application, follow these steps:
1. Clone the repository using the following command:
   ```
   git clone https://github.com/gilhotraapoorva/DeepFake_MultiFace_Videos.git

2. Navigate to the project directory:
```
cd DeepFake_MultiFace_Videos
```
3. Run the Flask application by executing the app2.py file:

```
python3 app2.py
```

4. Once the server is running, access the application by clicking on the "Try it now" button on the website.
5. Upload a video file by clicking on the "Choose file" button, then click on "Upload". The application will process the video and provide the result indicating the presence of deepfake manipulation.

## Disclaimer
This project is developed for educational and research purposes only. The accuracy and reliability of the deepfake detection algorithm may vary based on various factors, and it should not be solely relied upon for critical applications without proper validation and verification.

Feel free to contribute to this project by providing feedback, suggestions, or enhancements through pull requests or by raising issues.
