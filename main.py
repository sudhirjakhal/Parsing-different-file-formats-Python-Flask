from flask import Flask, request, render_template
import requests
import json
import xmltodict
from bs4 import BeautifulSoup


app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
def parse_files():
    if request.method == "POST":
        dtype = ''
        sample = ''
        status = ''
        url = request.form.get("URL")
        try:
            r = requests.get(url)
            r.raise_for_status()  # Raise exception for unsuccessful requests
        except requests.exceptions.HTTPError as e:
            status = f"HTTP Error: {e}"
            return render_template('index.html', status=status, url=url)
        except requests.exceptions.RequestException as e:
            status = f"Error: {e}"
            return render_template('index.html', status=status, url=url)

        status += str(r.status_code)
        content_type = r.headers.get("content-type")

        if "text/html" in content_type:
            soup = BeautifulSoup(r.content, 'html.parser')
            dtype = type(soup.prettify())
            sample = soup.prettify()[:int(len(soup.prettify())/5)]
        elif content_type == "application/xml":
            try:
                data = xmltodict.parse(r.content)
                dtype = 'Xml'
                sample = data
            except xmltodict.ExpatError as e:
                status = f"XML Parsing Error: {e}"
                return render_template('index.html', status=status, url=url)
        else:
            try:
                dic = json.loads(r.content)
                dtype = type(dic)
                sample = dic
            except json.JSONDecodeError as e:
                status = f"JSON Parsing Error: {e}"
                return render_template('index.html', status=status, url=url)
            except:
                status += f"\nInvalid URL. Try again with correct link. Thank you !"

        return render_template('index.html', status=status, url=url, datatype=dtype, preview=sample)
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
