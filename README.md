# Auto.am Message Sender

An automated message sending application for Auto.am with a user-friendly GUI interface. This tool helps users send personalized messages to car sellers based on specific search criteria using Selenium automation.

## Features

- **Automated Cookie Extraction**: Seamlessly extracts authentication cookies from Auto.am
- **Smart Message Management**: Add, remove, and manage multiple message templates
- **Advanced Search Filters**: Filter by category, price range, and page numbers
- **GUI Interface**: Easy-to-use Tkinter-based graphical interface
- **Headless Operation**: Option to run browser automation in background
- **Test Mode**: Safe testing environment before sending actual messages
- **Real-time Logging**: Monitor progress and status in real-time
- **Database Storage**: Persistent message storage using SQLite

## Requirements

- Python 3.7+
- Selenium WebDriver
- Chrome/Chromium browser
- ChromeDriver (compatible with your Chrome version)

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/RobertArustamyan/MessageSenderExe.git
   cd MessageSenderExe
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Download ChromeDriver**:
   - Download from [ChromeDriver Downloads](https://chromedriver.chromium.org/)
   - Place in your PATH or project directory
   - Ensure version matches your Chrome browser

## Usage

### Starting the Application

Run the main application:
```bash
python main.py
```

### Configuration Options

#### Authentication
- **Login**: Your Auto.am username
- **Password**: Your Auto.am password

#### Extraction Settings
- **Extract New Cookies**: Check to extract fresh authentication cookies
- **Cookie Extractor Headless**: Run cookie extraction in background
- **Message Sender Headless**: Run message sending in background

#### Search Parameters
- **Category**: Choose from available vehicle categories
  - All vehicles
  - Passenger cars
  - Trucks
  - Motorcycles
  - Special vehicles
  - Buses
  - Trailers
  - Water vehicles

- **Page Range**: Define start and end pages for search
- **Price Range**: Set minimum and maximum price filters (in USD)

#### Operation Modes
- **Send to All**: Send messages to all found listings
- **Test Mode**: Enable for safe testing without sending actual messages

### Message Management

1. **Adding Messages**: 
   - Type your message in the text field
   - Click "Add" or press Enter
   - Messages are stored in local database

2. **Removing Messages**:
   - Select message from the list
   - Click "Remove" button

### Running the Process

1. Configure all settings
2. Add at least one message template
3. Click "Start Process"
4. Monitor progress in the status log
5. Use "Stop" button to halt operation if needed
