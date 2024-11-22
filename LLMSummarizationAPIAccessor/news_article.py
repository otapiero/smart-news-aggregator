class NewsArticle:
    def __init__(self, title, body, image, url, dateTimePub, category):
        self.title = title
        self.body = body
        self.image = image
        self.url = url
        self.dateTimePub = dateTimePub
        self.category = category

    def __str__(self):
        return f"Title: {self.title}\nBody: {self.body}\nImage: {self.image}\nURL: {self.url}\nDate: {self.dateTimePub}\nCategory: {self.category}"

    def __repr__(self):
        return self.__str__()

    def to_dict(self):
        return {
            "title": self.title,
            "body": self.body,
            "image": self.image,
            "url": self.url,
            "dateTimePub": self.dateTimePub,
            "category": self.category,
        }

    def to_dict_for_llm(self):
        return {"title": self.title, "body": self.body}

    @staticmethod
    def from_dict(data):
        return NewsArticle(
            data["title"],
            data["body"],
            data["image"],
            data["url"],
            data["dateTimePub"],
            data["category"],
        )
