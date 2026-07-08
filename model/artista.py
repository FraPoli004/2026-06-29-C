from dataclasses import dataclass, field

@dataclass
class Artista:
    ArtistId: int
    Name: str
    brani: list = field(default_factory=list)
    playlist: list = field(default_factory=list)

    def __hash__(self):
        return hash(self.ArtistId)

    def __eq__(self, other):
        return self.ArtistId == other.ArtistId

    def __str__(self):
        return f"{self.Name}"