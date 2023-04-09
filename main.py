from flask  import Flask, request, render_template
import requests, json, xmltodict
from bs4 import BeautifulSoup


app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
def parse_files():
    if request.method == "POST":
        dtype = ''
        sample = ''
        url = request.form.get("URL")
        r = requests.get(url)
        r = requests.get(url)
        if "text/html" in r.headers["content-type"]:    
            soup = BeautifulSoup(r.content, 'html.parser')
            dtype = type(soup.prettify())
            sample = soup.prettify()[:int(len(soup.prettify())/5)]
        elif r.headers.get("content-type") == "application/xml":
            print("The response is in XML format")
            data = xmltodict.parse(r.content)
            print(data)
            dtype = 'Xml'
            sample = data
        else:
            print ("non html page")
            try:
                r.json()
                dic = json.loads(r.content)
                dtype = type(dic)
                sample = dic
            except:
                print('Not a json format')

        return render_template('index.html', status=r.status_code, url=url, datatype=dtype, preview=sample)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)