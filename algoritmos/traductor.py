# Módulo de traducción para el sistema de videojuegos

PALABRAS = {"turnos": "Turn-Based", "historia": "Story-Rich", "accion": "Action", "acción": "Action", "simulacion": "Simulation", "simulación": "Simulation", "aventura": "Adventure", "estrategia": "Strategy", "rol": "RPG", "gratis": "Free to Play", "disparos": "Shooter", "tiros": "Shooter", "terror": "Horror", "terror de supervivencia": "Survival Horror", "supervivencia": "Survival", "multijugador": "Multiplayer", "cooperativo": "Co-op", "cooperativo en línea": "Online Co-op", "cooperativo local": "Local Co-op", "competitivo": "Competitive", "mundo abierto": "Open World", "deportes": "Sports", "carreras": "Racing", "futbol": "Football (Soccer)", "fútbol": "Football (Soccer)", "fulbo": "Football (Soccer)", "pelotita": "Football (Soccer)", "beta": "Early Access", "acceso anticipado": "Early Access", "animación": "Animation", "animacion": "Animation", "violencia": "Violence", "vieja escuela": "Old School", "fisica": "Physics", "física": "Physics", "sigilo": "Stealth", "combate": "Combat", "combate cuerpo a cuerpo": "Melee Combat", "tercera persona": "Third Person", "primera persona": "First Person", "cartas": "Card Game", "rompe cabezas": "Puzzle", "rompecabezas": "Puzzle", "realista": "Realistic", "plataforma": "Platformer", "defensa de torres": "Tower Defense", "satira": "Satire", "sátira": "Satire", "educativo": "Educational", "sangre": "Blood", "comedia": "Comedy", "novetas": "1990s", "ritmo": "Rhythm", "apuestas": "Gambling", "casuales": "Casual", "relajante": "Relaxing", "tierno": "Cute", "clasico": "Classic", "clásico": "Classic", "zombie": "Zombies", "zombis": "Zombies", "cagalos a tiros": "Shoot Em Up", "tiritos": "Shoot Em Up", "economia": "Economy", "economía": "Economy", "crafteo": "Crafting", "exploracion": "Exploration", "exploración": "Exploration", "realidad virtual": "VR", "realidad aumentada": "AR", "mechas": "Mechs", "abstracto": "Abstract", "novela visual": "Visual Novel", "juego de mesa": "Board Game", "inclusivo": "LGBTQ+", "buena musica": "Great Soundtrack", "musica piola": "Great Soundtrack", "espacio": "Space", "humor negro": "Dark Humor", "amor": "Romance", "citas": "Dating Sim", "afk": "Idler", "crimenes": "Crime", "tactica": "Tactical"}


class Traductor:
    """Clase para traducir etiquetas del español al inglés."""

    @staticmethod
    def traducir(etiqueta: str) -> str:
        """Traduce una etiqueta del español al inglés.

        Si la etiqueta ya está en inglés o no se conoce, se devuelve tal cual,
        para que la búsqueda nunca reciba un valor nulo.
        """
        etiqueta = etiqueta.strip().lower()
        return PALABRAS.get(etiqueta, etiqueta)
