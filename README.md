## Medium Automation with Deepseek and Python

A simple Python-based project to generate stories using the Deepseek API and publish them on Medium via automated Chrome browser sessions. Designed for educational purposes and easy extension.

---

### Features

- Generate stories using Deepseek
- Automate Medium login and publishing with selenium
- Modular, maintainable code structure

---

### Prerequisites

- Python 3.8+ installed
- A Deepseek key from Openrouter
- A Medium account from Facebook (email & password)
- Google Chrome installed

---

### Setup

1. **Clone the repo**

   ```bash
   git clone https://github.com/vyn-7/medium_automation.git
   cd medium_automation
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Create a `.env` file** in project root with the following:

   ```ini
   API_KEY=your_api_key
   MEDIUM_EMAIL=you@example.com
   ```

---

### Usage

Edit the prompt in `main.py` or pass your own via CLI:

```bash
python main.py
```

The script will:

1. Generate a random story
2. Launch selenium and login to Medium
3. Publish the generated story

---

Happy automating! 🚀
