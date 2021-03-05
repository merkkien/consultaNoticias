class headline:
    def __init__(self, id, title, datePublished, description, tags, resume):
        self.id = id
        self.title = title
        self.datePublished = datePublished
        self.description = description
        self.tags = tags
        self.resume = resume
    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'datePublished': self.datePublished,
            'description': self.description,
            'tags': ','.join(map(str, self.tags)) ,
            'resume': self.resume,
        }

