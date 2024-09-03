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
### Setup the Flask Server
  - ```
    cd Model
    ```
    ```
    pip install -r requirements.txt
    ```
### Running the NodeJS Server
  - ```
    cd JavaScriptServer
    ```
    ```
    npm start
    ```
### Running the Flask Server
  - ```
    cd Model
    ```
    ```
    python app.py
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
