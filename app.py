from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)

# Herní deska a proměnné pro správu hry
deska = [None] * 9
na_tahu = "X"  # "X" začíná
vitez = None  # Uchovává vítěze ("X" nebo "O") nebo None, pokud zatím není vítěz

# Funkce pro kontrolu výherních řad
def zjisti_vyhru():
    global vitez
    # Výherní kombinace
    vyherni_kombinace = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),  # horizontální řady
        (0, 3, 6), (1, 4, 7), (2, 5, 8),  # vertikální řady
        (0, 4, 8), (2, 4, 6)              # diagonální řady
    ]
    
    # Kontrola, zda některá výherní kombinace obsahuje stejné symboly
    for a, b, c in vyherni_kombinace:
        if deska[a] == deska[b] == deska[c] and deska[a] is not None:
            vitez = deska[a]
            return True
    return False

@app.route('/')
def index():
    return render_template('game.html', deska=deska, na_tahu=na_tahu, vitez=vitez)

@app.route('/tah/<int:index>', methods=['POST'])
def tah(index):
    global deska, na_tahu, vitez
    
    # Kontrola, zda je tah platný a jestli už někdo nevyhrál
    if deska[index] is None and vitez is None:
        deska[index] = na_tahu  # Nastavení tahu
        if zjisti_vyhru():  # Kontrola výhry
            return redirect(url_for('index'))
        
        # Přepnutí na druhého hráče, pokud není vítěz
        na_tahu = "O" if na_tahu == "X" else "X"
    
    return redirect(url_for('index'))

@app.route('/reset')
def reset():
    global deska, na_tahu, vitez
    deska = [None] * 9
    na_tahu = "X"
    vitez = None
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=8080)
