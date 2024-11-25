def format_email_content(articles):
    email_html = """
    <html>
    <body>
        <h2>Your Personalized News</h2>
        {}
    </body>
    </html>
    """
    article_html = """
    <div style="margin-bottom: 20px;">
        <h3>{title}</h3>
        <img src="{image}" alt="Article Image" style="width:100%; max-width:600px;"/>
        <p>{body}</p>
        <a href="{url}" target="_blank">Read more</a>
    </div>
    """
    formatted_articles = [
        article_html.format(
            title=article["title"],
            body=article["body"],
            image=article["image"],
            url=article["url"],
        )
        for article in articles
    ]
    return email_html.format("".join(formatted_articles))
