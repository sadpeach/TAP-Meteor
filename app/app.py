from household import app
import os

if __name__ == '__main__':
    from waitress import serve
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5001)), debug=True)
    # serve(app, host="0.0.0.0",port=int(os.environ.get('PORT', 5001)))