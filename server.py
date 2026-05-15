from flask import Flask, request, jsonify
import sqlite3
import gemini_manager
app = Flask(__name__)

@app.route('/get', methods=['GET'])
def get_test():
    connection = sqlite3.connect('Data.db')
    cursor = connection.cursor()
    word = request.args.get('word')
    cursor.execute("SELECT * FROM Fignya_Melkaya where word = ?", (word,))
    all_rows = cursor.fetchall()
    if all_rows:
        return jsonify({'word': all_rows[0][2]})
    else:
        gemini_response = gemini_manager.get_response(word)
        print(gemini_response, word)
        if gemini_response != "no":
            cursor.execute("INSERT INTO Fignya_Melkaya (word, meaning) VALUES (?, ?)", (word, gemini_response[4:]))
        connection.commit()
        return gemini_response[4:]


if __name__ == '__main__':
    app.run(port=6767)
