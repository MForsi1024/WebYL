from flask import Flask, request, jsonify
import sqlite3
import gemini_manager

app = Flask(__name__)


@app.route('/get', methods=['GET'])
def get_test():
    connection = sqlite3.connect('Data.db')
    cursor = connection.cursor()
    word = request.args.get('word')
    cursor.execute("SELECT id, word, meaning FROM Fignya_Melkaya where word = ?", (word,))
    all_rows = cursor.fetchall()
    if all_rows:
        cursor.execute("UPDATE Data SET count = count + 1 WHERE word = ?", (word,))
        connection.commit()
        connection.close()
        print(all_rows)
        return jsonify({'word': all_rows[0][2]})
    else:
        gemini_response = gemini_manager.get_response(word)
        print(gemini_response, word)
        if gemini_response != "no" or not gemini_response:
            cursor.execute("INSERT INTO Data (word, meaning, count) VALUES (?, ?, ?)",
                           (word, gemini_response[4:], 1))
            connection.commit()
            connection.close()
            return jsonify({gemini_response[4:]})

        connection.commit()
        connection.close()
        return jsonify({'word': "К сожалению я на такое не отвечу. Давай другое слово попробуем."})


if __name__ == '__main__':
    app.run(port=6767)
