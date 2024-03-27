from flask import Flask, jsonify, request, Response, render_template
import requests
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search')
def search():
    query = request.args.get('query')
    if query:
        response = requests.get(f'https://api.github.com/search/repositories?q={query}')
        return jsonify(response.json())
    else:
        return jsonify([])

@app.route('/download')
def download():
    url = request.args.get('url')
    if url:
        download_url = url.replace('api.github.com/repos', 'github.com').replace('/{archive_format}{/ref}', '/archive/master.zip')
        try:
            response = requests.get(download_url, allow_redirects=True)
            if response.status_code == 200:
                return Response(
                    response.content,
                    headers={
                        'Content-Disposition': 'attachment; filename=generatedcode.zip',
                        'Content-Type': 'application/zip'
                    }
                )
            else:
                return f"Error downloading zip file: {response.status_code}"
        except Exception as e:
            return f"Error downloading zip file: {str(e)}"
    else:
        return "Invalid URL"
    
if __name__ == '__main__':
    app.run(debug=True)
