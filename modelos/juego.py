class Juego:
    def __init__(self, titulo, tags, rating):
        self._titulo = titulo
        self._tags = tags 
        self._rating = rating


    @property
    def titulo(self):
        return self._titulo
    
    @property
    def tags(self):
        return self._tags
    
    @property
    def rating(self):
        return self._rating

    @property
    def jugado(self):
        return self._jugado

    
    def __repr__(self):
        return f"{self._titulo} ⭐{self._rating} ({', '.join(self._tags)})"


