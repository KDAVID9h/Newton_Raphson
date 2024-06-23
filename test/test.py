import speech_recognition as sr
import sympy as sp

# Dictionnaire pour mapper les mots aux symboles mathématiques
math_map = {
    'un': '1',
    'deux': '2',
    'trois': '3',
    'quatre': '4',
    'cinq': '5',
    'six': '6',
    'sept': '7',
    'huit': '8',
    'neuf': '9',
    'zéro': '0',
    'fois': '*',
    'plus': '+',
    'moins': '-',
    'divisé': '/',
    'au carré': '**2',
    'racine carrée': 'sqrt',
    'ln': 'log',
    'log': 'log10',
    'expo': 'exp'
}

# Initialiser la reconnaissance vocale
recognizer = sr.Recognizer()

def recognize_speech():
    with sr.Microphone() as source:
        print("Dites quelque chose :")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio, language="fr-FR")
            print(f"Vous avez dit : {text}")
            return text
        except sr.UnknownValueError:
            print("Désolé, je n'ai pas compris.")
        except sr.RequestError:
            print("Erreur de service ; veuillez réessayer.")

def process_text(text):
    words = text.split()
    processed_words = []
    for word in words:
        if word in math_map:
            processed_words.append(math_map[word])
        else:
            processed_words.append(word)
    return ' '.join(processed_words)

def evaluate_expression(expression):
    try:
        # Remplacer les fonctions mathématiques spéciales par celles de sympy
        expression = expression.replace('sqrt', 'sp.sqrt')
        expression = expression.replace('log', 'sp.log')
        expression = expression.replace('log10', 'sp.log10')
        expression = expression.replace('exp', 'sp.exp')
        
        # Evaluation de l'expression
        result = eval(expression)
        return result
    except Exception as e:
        return f"Erreur dans l'évaluation de l'expression: {e}"

if __name__ == "__main__":
    while True:
        spoken_text = recognize_speech()
        if spoken_text:
            formatted_text = process_text(spoken_text)
            print(f"Expression formatée : {formatted_text}")
            result = evaluate_expression(formatted_text)
            print(f"Résultat : {result}")
