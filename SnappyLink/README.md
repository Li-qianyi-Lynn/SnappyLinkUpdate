# SnappyLink

**SnappyLink** is a web application that allows users to generate short links and QR codes from long URLs. It simplifies sharing long and complex URLs, making it easy for users to embed these in marketing materials, SMS, emails, or social media. SnappyLink ensures that users have a quick, accessible way to manage their URLs in a simple, user-friendly interface.

Please visit our website: http://i16k.com/, which is deployed on AWS EC2 and is accessible globally.

## Features

- **Short Link Generation**: Convert long URLs into unique, easy-to-share short links.
- **QR Code Generation**: Generate QR codes for each short link, making it easy to share visually.
- **Link Management**: Store, retrieve, and manage long URLs and their corresponding short links using MySQL.
- **Visit Count**: Track the number of visits to each short link, providing usage statistics.
- **Responsive Design**: User interface designed to adapt to different device sizes, ensuring optimal user experience across desktop, tablet, and mobile.
- **Cloud Deployment**: Application hosted on AWS EC2 to provide global access and high availability.

## Technologies Used

- **Backend**:
  - **Flask**: A lightweight web framework used to handle HTTP requests, routing, and rendering pages.
  - **SQLAlchemy & MySQL**: For database management, providing persistent data storage and easy data handling.
  - **shortuuid**: Library used to generate unique short codes for URLs, ensuring no hash collisions.
  - **qrcode**: For generating QR codes to accompany each short link.
  - **logging**: `snappy_link.log` for tracking and debugging purposes, ensuring system stability and transparency.

- **Frontend**:
  - **HTML (generate.html in templates folder)**: Provides the basic structure and content of the web pages.
  - **Bootstrap**: To create a responsive user interface that works well across various devices.

- **Deployment**:
  - **AWS EC2**: Deployed on Amazon's cloud platform for scalability, stability, and global accessibility.

## Installation

1. Open the folder **SnappyLink**:
   
   - Directly open the project folder on your computer by PyCharm or any other IDE (Visual Studio Code,etc.), ensuring all files remain in their original structure.
   - Define python version
     - Python 3.10.15 or 
     - Python 3.12.4 

2. Create a Virtual Environment:
   ```
   python3 -m venv snappylink_env
   source snappylink_env/bin/activate  # On Windows, use `snappylink_env\Scripts\activate`
   ```

3. Install Python Dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Run the Application:
   ```
   flask --app snappy_link run # Or run "python3 snappy_link.py"
   ```

5. Press CTRL+C to quit.

The application will be available at http://127.0.0.1:5000 or http://127.0.0.1:80  .

## Project Structure

- **static/**: Contains static files like CSS, images, and JavaScript.
- **templates/**: Contains HTML templates (e.g., `generate.html`) used for rendering pages.
- **venv/**: Virtual environment directory containing installed dependencies.
- **.gitignore**: Specifies files and directories that should be ignored by Git.
- **README.md**: Guidebook for the project.
- **requirements.txt**: Lists the Python dependencies needed for the project.
- **snappy_link.py**: Backend logic of the application (Flask server).
- **snappy_link.log**: Log file for tracking and debugging.

## Contributors

- Meizhui Xu 002062406 NEU
- Qianyi Li 002053228 NEU


---

We hope you find SnappyLink useful for managing and sharing your URLs effectively!
