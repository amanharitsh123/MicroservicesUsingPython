from flask import Flask, render_template, request, redirect, url_for
import jinja2
import requests

app = Flask(__name__)

@app.route("/products/admin", methods=["GET", "POST"])
def admin():
    data = requests.get("http://172.17.0.1:8000/api/products")
    data = data.json()
    loader = jinja2.FileSystemLoader('templates/table.html')
    env = jinja2.Environment(loader=loader)
    template = env.get_template('')
    return template.render(items=data)

@app.route("/products/create", methods=["POST"])
def create():
    result = request.form.to_dict(flat=False)
    data = {'title':result['title'][0], 'image':result['image'][0]}
    requests.post("http://172.17.0.1:8000/api/products", data=data)
    return redirect(url_for('admin'))

@app.route("/products/delete", methods=["POST", "GET"])
def delete():
    result = request.form.to_dict(flat=False)
    print(result)
    requests.delete("http://172.17.0.1:8000/api/products/"+result['id'][0])
    return redirect(url_for('admin'))

@app.route("/products/update", methods=["POST"])
def update():
    result = request.form.to_dict(flat=False)
    id = result['id'][0]
    data = {'title':result['title'][0], 'image':result['image'][0]}
    requests.put("http://172.17.0.1:8000/api/products/"+id, data=data)
    return redirect(url_for('admin'))

@app.route("/products/like", methods=["POST"])
def like():
    result = request.form.to_dict(flat=False)
    id = result['id'][0]
    requests.post("http://172.17.0.1:8001/api/products/"+id + "/like")
    return redirect(url_for('admin'))



if __name__ == "__main__":
    app.run(host='0.0.0.0', port="5001", debug=True)