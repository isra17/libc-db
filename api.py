from flask import Flask, request
from tools.libdownloader import LibDownloader
from tools.elfsymbolsparser import ElfSymbolsParser
from model.libc_binary import LibcBinary

app = Flask(__name__)

@app.route("/")
def list():
    return "Empty"

@app.route("/analyze", methods=["POST"])
def analyze():
    target = request.form['target']

    downloader = LibDownloader(target)
    download_target = downloader.download()

    parser = ElfSymbolsParser(open(downloader.location, 'rb'))
    lib = parser.parse_all()
    download_info.lib_binary = lib;

    return 'Ok'

if __name__ == "__main__":
    app.run(debug=True)

