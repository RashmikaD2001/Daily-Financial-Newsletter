from finance_news import getData, getNews
from agent import news_generator
from emails import send_email
from template import build_email_template
import yaml

if __name__ == "__main__":
    with open("email.yaml", "r") as f:
        config = yaml.safe_load(f)
        recipient_email_list = config["recipients"]  # already a list

    news = getNews()
    data = getData(news)

    newsletter = news_generator(news_data=data)
    email_body = build_email_template(newsletter)
    send_email(recipient_email_list, email_body)

    