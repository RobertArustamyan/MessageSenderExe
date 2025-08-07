# Auto.am Message Sender

An automated message sending application for Auto.am with a user-friendly GUI interface. This tool helps users send personalized messages to car sellers based on specific search criteria using Selenium automation.

## 🚗 Features

- **Automated Cookie Extraction**: Seamlessly extracts authentication cookies from Auto.am
- **Smart Message Management**: Add, remove, and manage multiple message templates
- **Advanced Search Filters**: Filter by category, price range, and page numbers
- **GUI Interface**: Easy-to-use Tkinter-based graphical interface
- **Headless Operation**: Option to run browser automation in background
- **Test Mode**: Safe testing environment before sending actual messages
- **Real-time Logging**: Monitor progress and status in real-time
- **Database Storage**: Persistent message storage using SQLite

## 📋 Requirements

- Python 3.7+
- Selenium WebDriver
- Chrome/Chromium browser
- ChromeDriver (compatible with your Chrome version)

## 🛠️ Installation

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

## 🚀 Usage

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

## 📁 Project Structure

```
MessageSenderExe/
├── main.py                     # Main GUI application
├── CookieExtraction/
│   └── cookie_extractor.py     # Cookie extraction module
├── Messages/
│   ├── message_sender.py       # Message sending logic
│   └── messages.py             # Message and database management
├── AppData/
│   ├── cookies.pkl             # Stored authentication cookies
│   └── messages.db             # SQLite message database
└── README.md
```

## 🔧 Module Overview

### CookieExtractor
Handles authentication and cookie extraction from Auto.am using Selenium WebDriver.

### MessageSender/CustomSender
Core automation engine that:
- Navigates through Auto.am listings
- Applies search filters
- Sends messages to sellers
- Provides progress callbacks to GUI

### Messages & MessageDatabase
- Manages message templates
- Provides SQLite database storage
- Handles CRUD operations for messages

## ⚠️ Important Notes

### Safety Features
- **Test Mode**: Always test your setup before live operation
- **Rate Limiting**: Built-in delays to avoid overwhelming the server
- **Error Handling**: Comprehensive error catching and reporting

### Best Practices
1. Start with test mode enabled
2. Use reasonable page ranges to avoid excessive requests
3. Keep messages professional and relevant
4. Respect Auto.am's terms of service
5. Monitor logs for any issues or errors

### Legal Compliance
- Ensure compliance with Auto.am's terms of service
- Use responsibly and ethically
- Avoid spamming or excessive automated requests
- Respect other users' privacy and preferences

## 🐛 Troubleshooting

### Common Issues

**ChromeDriver Version Mismatch**:
- Update ChromeDriver to match your Chrome browser version
- Check Chrome version: `chrome://version/`

**Cookie Extraction Fails**:
- Verify login credentials
- Try running with headless mode disabled
- Check for website layout changes

**Messages Not Sending**:
- Ensure cookies are valid and recent
- Verify search parameters return results
- Check network connectivity

**GUI Not Responding**:
- Threading issues - restart the application
- Check Python version compatibility

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚖️ Disclaimer

This tool is for educational and automation purposes. Users are responsible for:
- Complying with Auto.am's terms of service
- Following applicable laws and regulations
- Using the tool ethically and responsibly
- Obtaining proper permissions where required

The developers are not responsible for any misuse or violations of terms of service.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📞 Support

If you encounter any issues or have questions:
- Open an issue on GitHub
- Check the troubleshooting section above
- Review the code documentation

---

**⭐ If this project helped you, please give it a star on GitHub!**