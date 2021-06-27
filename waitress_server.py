from waitress import serve
import src.main
serve(src.main.app, host='0.0.0.0', port=8000, threads=4)