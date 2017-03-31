# -*- coding: utf-8
from flask import Flask, render_template, request
from cparse import do_parse
import json


app = Flask(__name__)


app.jinja_env.add_extension('jinja2.ext.do')


@app.template_filter('to_json')
def filter_to_json(d):
    return json.dumps(d, ensure_ascii=False)


@app.template_filter('default_icon')
def filter_default_icon(i):
    if i:
        d = i
    else:
        d = "fa-list"
    return d


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload/<model>')
def upload(model):
    return render_template('upload.html', model=model)


@app.route('/parse/<model>', methods=['GET', 'POST'])
def parse(model):
    r = do_parse(model, request.files['file'])
    cc = sorted(r[0].values(), key=lambda k: k['layer'], reverse=True)
    return render_template('dev.html', cc=cc, devname=model, unknown=r[1])


@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def internal_error(e):
    return render_template("errors/500.html", error=e), 500

if __name__ == '__main__':
    app.run()
