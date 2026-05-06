import logging

import openai
from django.conf import settings

logger = logging.getLogger(__name__)


class AIService:
    """Service centralisé pour gérer les interactions avec OpenAI."""
    
    def __init__(self):
        self.client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = "gpt-4o-mini"

    def generate_cover_letter(self, user_data, job_description):
        """Génère une lettre de motivation personnalisée."""
        prompt = f"""
        Rédige une lettre de motivation professionnelle en français.
        Profil du candidat : {user_data}
        Description du poste : {job_description}
        Format: Professionnel, structuré, maximum 400 mots.
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Tu es un expert en recrutement et en rédaction professionnelle."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=800
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"OpenAI error: {e}")
            return None

    def improve_content(self, text, context="professionnel"):
        """Améliore le style et la grammaire d'un texte existant."""
        # Logique similaire pour l'amélioration de CV...
        pass