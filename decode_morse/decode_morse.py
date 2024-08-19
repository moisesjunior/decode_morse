import os
import sys
import datetime
import pandas as pd
from config import file_path, dict_morse

# Invertendo o dicionário de Morse para texto
dict_morse_inv = {v: k for k, v in dict_morse.items()}

def decode_morse(msg):
    '''
    input : mensagem em código morse com letras separadas por espaços e palavras por dois espaços
    output : palavra escrito em letras e algarismos
    '''
    words = msg.split("  ")  # Divide em palavras
    decoded_words = []
    
    for word in words:
        letters = word.split(" ")  # Divide em letras
        decoded_letters = [dict_morse.get(letter, '?') for letter in letters]  # Decodifica cada letra
        decoded_words.append("".join(decoded_letters))
    
    return " ".join(decoded_words)

def encode_morse(text):
    '''
    input : mensagem em texto
    output : mensagem em código morse com letras separadas por espaços e palavras por dois espaços
    '''
    text = text.upper()
    encoded_words = []
    
    for word in text.split():
        encoded_letters = [dict_morse_inv.get(char, '') for char in word]  # Codifica cada letra
        encoded_words.append(" ".join(encoded_letters))
    
    return "  ".join(encoded_words)

def save_to_csv(msg, file_name):
    '''
    input : mensagem em texto e nome do arquivo
    output : salva a mensagem em um arquivo csv
    '''
    now = datetime.datetime.now()
    df = pd.DataFrame([[msg, now]], columns=["mensagem", "datetime"])
    hdr = not os.path.exists(file_name)
    df.to_csv(file_name, mode="a", index=False, header=hdr)

def is_morse_code(msg):
    '''
    Checa se a mensagem é código Morse.
    Assumimos que o código Morse contém apenas '.' e '-' e espaços.
    '''
    return all(char in '.- ' for char in msg)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        input_text = sys.argv[1]
        
        if is_morse_code(input_text):
            # Se a entrada é código Morse, decodificar
            msg_claro = decode_morse(input_text)
            print(f"Mensagem decodificada: {msg_claro}")
            save_to_csv(msg_claro, file_path)
            
            # Codificar a mensagem decodificada para verificar a reversibilidade
            encoded_msg = encode_morse(msg_claro)
            print(f"Mensagem codificada: {encoded_msg}")
            save_to_csv(encoded_msg, 'encoded_morse.csv')
        else:
            # Se a entrada é texto, codificar
            encoded_msg = encode_morse(input_text)
            print(f"Mensagem codificada: {encoded_msg}")
            save_to_csv(encoded_msg, 'encoded_morse.csv')
            
            # Decodificar a mensagem codificada para verificar a reversibilidade
            msg_claro = decode_morse(encoded_msg)
            print(f"Mensagem decodificada: {msg_claro}")
            save_to_csv(msg_claro, file_path)
    else:
        print("Por favor, forneça uma mensagem como argumento.")
