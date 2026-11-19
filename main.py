"""Executa o módulo de Energia do Citizen Assist AI de forma independente.

Uso:
    python main.py                       menu interativo
    python main.py --demo                demonstração (usada no vídeo)
    python main.py --pergunta "texto"    uma pergunta direta
"""
import argparse

from energia.assistente import menu_energia, responder


def demo():
    for pergunta in ("Quanto minha casa consome?", "Como reduzir minha conta de luz?", "E o painel solar, vale a pena?"):
        print("\n>>> " + pergunta)
        print(responder(pergunta))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Citizen Assist AI - módulo de Energia")
    ap.add_argument("--demo", action="store_true", help="executa a demonstração")
    ap.add_argument("--pergunta", help="faz uma pergunta e mostra a resposta")
    args = ap.parse_args()
    if args.demo:
        demo()
    elif args.pergunta:
        print(responder(args.pergunta))
    else:
        menu_energia()
