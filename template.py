import markdown
from datetime import date, timedelta

def build_email_template(newsletter_body_md: str):
    # Convert Markdown summary to HTML
    newsletter_body_html = markdown.markdown(newsletter_body_md)

    today = date.today()
    yesterday = today - timedelta(days=1)
    return f"""
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 20px;
                background-color: #f4f4f4;
            }}
            .container {{
                max-width: 800px;
                margin: auto;
                background: #ffffff;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0px 2px 8px rgba(0,0,0,0.1);
            }}
            h1, h2, h3 {{
                color: #2c3e50;
                margin-top: 20px;
                border-bottom: 1px solid #eee;
                padding-bottom: 5px;
            }}
            ul {{
                padding-left: 20px;
            }}
            li {{
                margin-bottom: 8px;
                line-height: 1.5;
            }}
            p {{
                color: #555;
                line-height: 1.6;
            }}
            .footer {{
                margin-top: 30px;
                font-size: 12px;
                color: #888;
                text-align: center;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📊 Daily Financial Newsletter</h1>
            <p><strong>Date:</strong> {yesterday}</p>

            {newsletter_body_html}

            <div class="footer">
                <p>You are receiving this newsletter because you subscribed to Financial Updates.</p>
                <p>© {today.year} Finance News Agent</p>
            </div>
        </div>
    </body>
    </html>
    """
