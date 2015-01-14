from flask import Flask, request
from tools.libdownloader import LibDownloader
from tools.elfsymbolsparser import ElfSymbolsParser

app = Flask(__name__)

@app.route("/")
def list():
    return "Empty"

@app.route("/analyze", methods=["POST"])
def analyze():
    target = request.form['target']
    downloader = LibDownloader(target)
    parser = ElfSymbolsParser(open(downloader.location, 'rb'))
    Symbol.insert_symbols(parser.symbols_table)
    return 'Ok'

if __name__ == "__main__":
    app.run(debug=True)

