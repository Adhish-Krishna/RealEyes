# RealEyes - Multi Model Deepfake Detection System

## Installation

### Clone the repository
  - ```
    git clone https://github.com/Adhish-Krishna/RealEyes.git
    ```
    ```
    cd RealEyes
    ```
### Setup the NodeJS Server
  - ```
    cd JavaScriptServer
    ```
    ```
    npm i
    ```
### Setting up and running the Flask Servers
-   **Download Models from Drive:**
    - ***Audio Deepfake Detection Service:***
      - Downlaod the folder from [here](https://drive.google.com/drive/folders/1EWklqA0wg0rnZWeryTW4dxbAw76lbRjU?usp=sharing) and place it inside `DeepfakeAudioDetection` folder.
      - The folder structure should be like this `DeepfakeAudioDetection/wav2vec2-base-finetuned-ks/checkpoint-841`
    - ***AI Text Detection service:***
      - Downlaod the files from [here](https://drive.google.com/drive/folders/1fDZMmW6jVsaXM_EkJBCHU1Sm9Gk-7F4h?usp=sharing) and place them inside `text_detection/final_model` folder.

-   **Setting up Deepfake Image/Video Detection Service:**
    - ```
      cd Model
      ```
      ```
      pip install requirements.txt
      ```
      ```
      python app.py
      ```

-   **Setting up Deepfake Audio Detection Service:**
    - ```
      cd DeepfakeAudioDetection
      ```
      ```
      python app.py
      ```

-   **Setting up AI Text Detection Service:**
    - ```
      cd text_detection
      ```
      ```
      pip install requirements.txt
      ```
      ```
      python servercheck.py
      ```

### Running the NodeJS Server
  - ```
    cd JavaScriptServer
    ```
    ```
    npm start
    ```
### Accessing RealEyes
  - Visit http://localhost:3000 to access RealEyes

### Installing the Browser Extension
1. **Download the Extension**:
   - Clone or download the `BrowserExtension` folder

2. **Open Chrome Extensions Page**:
   - Open Chrome and go to `chrome://extensions/`.

3. **Enable Developer Mode**:
   - Toggle the "Developer mode" switch in the top right corner.

4. **Load Unpacked Extension**:
   - Click on the "Load unpacked" button and select the `BrowserExtension` folder where the extension files are located.

5. **Verify Installation**:
   - Ensure the extension appears in the list of installed extensions and is enabled.

### Usage of the browser extension:
   - After successfuly installing the extension, you can right click on any image and video on the web and select "Detect Deepfake" option. After few seconds the results will be displayed on a new html page
