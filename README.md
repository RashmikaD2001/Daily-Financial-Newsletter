# 📊 Daily Financial Newsletter

An automated AI-powered financial newsletter system that fetches financial news, analyzes company data, and sends comprehensive daily email summaries using LangChain agents and Google's Gemini AI.

## Features

- **Automated News Fetching**: Retrieves latest financial news from Financial Modeling Prep API
- **AI-Powered Analysis**: Uses Google Gemini 2.0 Flash with LangChain agents for intelligent analysis
- **Multi-Tool Integration**: 
  - Wikipedia for company background research
  - Yahoo Finance for stock data and news
  - Built-in calculator for financial computations
- **Automated Email Delivery**: Sends formatted HTML newsletters via SMTP
- **GitHub Actions Automation**: Scheduled daily execution
- **Error Handling**: Admin notifications for failed runs

## Architecture

The system consists of several interconnected modules:

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│ News API    │────▶│  Data Fetch  │────▶│   Agent     │
│  (FMP)      │     │  (yfinance)  │     │ (LangChain) │
└─────────────┘     └──────────────┘     └─────────────┘
                                                │
                                                ▼
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│ Recipients  │◀────│ Email Sender │◀────│  Template   │
│  (YAML)     │     │   (SMTP)     │     │  Builder    │
└─────────────┘     └──────────────┘     └─────────────┘
```

## Prerequisites

- Python 3.11+
- Gmail account (or other SMTP server)
- API Keys:
  - Google Gemini API key
  - Financial Modeling Prep API key

## Installation

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd finance-newsletter
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_gemini_api_key
NEWS_API_KEY=your_fmp_api_key
EMAIL_ADDRESS=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
ADMIN_EMAIL=admin@email.com
```

**Note**: For Gmail, use an [App Password](https://support.google.com/accounts/answer/185833) instead of your regular password.

4. **Configure email recipients**

Create an `email.yaml` file:

```yaml
recipients:
  - recipient1@example.com
  - recipient2@example.com
  - recipient3@example.com
```

## Project Structure

```
.
├── main.py                 # Main orchestration script
├── agent.py               # LangChain agent configuration
├── finance_news.py        # News fetching and data retrieval
├── emails.py              # Email sending functionality
├── template.py            # HTML email template builder
├── email.yaml             # Recipient list configuration
├── .env                   # Environment variables (not committed)
├── .github/
│   └── workflows/
│       └── python-app.yml # GitHub Actions workflow
└── requirements.txt       # Python dependencies
```

## Usage

### Local Execution

Run the newsletter manually:

```bash
python main.py
```

### Automated Execution (GitHub Actions)

The project includes a GitHub Actions workflow that runs daily at 4:00 PM UTC.

**Setup Steps**:

1. **Add Repository Secrets**

   Go to your GitHub repository → Settings → Secrets and variables → Actions

   Add the following secrets:

   - `EMAIL_YAML_CONTENT`: Complete contents of your `email.yaml` file
   - `DOTENV_CONTENT`: Complete contents of your `.env` file

2. **Enable GitHub Actions**

   Ensure GitHub Actions are enabled in your repository settings.

3. **Manual Trigger**

   You can manually trigger the workflow from the Actions tab using the "Run workflow" button.

### Customize Schedule

Edit `.github/workflows/newsletter.yml`:

```yaml
on:
  schedule:
    - cron: "00 16 * * *"  # 4:00 PM UTC daily
```

## How It Works

1. **Fetch News**: Retrieves latest financial articles from Financial Modeling Prep API
2. **Enrich Data**: For each article, fetches company stock data using yfinance
3. **AI Analysis**: LangChain agent analyzes the data using:
   - Wikipedia for company background
   - Calculator for financial metrics
   - Yahoo Finance for additional context
4. **Generate Newsletter**: Gemini AI creates a comprehensive summary
5. **Format & Send**: Converts markdown to HTML and emails to all recipients
6. **Error Handling**: If errors occur, admin receives notification

## API Documentation

### Financial Modeling Prep API
- Endpoint: `https://financialmodelingprep.com/stable/fmp-articles`
- Returns: Latest financial news articles with ticker symbols

### yfinance
- Fetches real-time stock information and historical data
- No API key required

## Customization

### Modify Agent Behavior

Edit the system prompt in `agent.py`:

```python
prompt_template = ChatPromptTemplate.from_messages([
    ("system", "Your custom instructions here..."),
    ("user", "{news_data}")
])
```

### Change Email Template

Modify the HTML structure in `template.py`:

```python
def build_email_template(newsletter_body_md: str):
    # Customize your email design here
    pass
```

### Add More Tools

Extend the agent's capabilities in `agent.py`:

```python
from langchain_community.tools import SomeNewTool

new_tool = SomeNewTool()
tools = [wikipedia, math_tool, yahoo_fin, new_tool]
```

## Dependencies

Key packages:
- `langchain` - Agent framework
- `langchain-google-genai` - Gemini AI integration
- `yfinance` - Stock data retrieval
- `python-dotenv` - Environment management
- `markdown` - HTML conversion
- `pyyaml` - Configuration parsing

See `requirements.txt` for complete list.
---

**Made with ❤️ for automated financial intelligence**
