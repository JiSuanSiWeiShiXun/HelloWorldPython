import tempfile
import zipfile
import shutil
import csv
import os
import json
import time
import base64
import requests
from flask import Flask, send_file, request, jsonify
import sys
import platform
from optparse import OptionParser

app = Flask(__name__)




@app.route("/remove_minio_dir", methods=["POST", "GET"])
def RemoveMinioDir():
    dir_name = None
    pid = None
    email = None


    if request.form.get('dir_name', None):
        dir_name = request.form.get('dir_name', None)
 
    if request.form.get('pid', None):
        pid = request.form.get('pid', None)

    if request.form.get('email', None):
        email = request.form.get('email', None)

    if not dir_name or len(dir_name) < 1 or dir_name.find('*') != -1:
        return jsonify({"ret": -1, "err": "dir_name not current"})

    d_name = '/home/data/' + pid + '/' + dir_name
    if not os.path.exists(d_name):
        return jsonify({"ret": -1, "err": "dir_name not exist"})

    shutil.rmtree(d_name)


    return jsonify({"ret": 0, "err": "ok"})


@app.route("/query_project_config", methods=["POST", "GET"])
def QueryProjectConfig():
    json_conf = {}
    projectid = None

    if request.form.get('projectid', None):
        projectid = request.form.get('projectid', None)

    if not projectid :
        return jsonify({"json_conf": json_conf})

    d_name = '/home/data/' + projectid + '/.snake'
    if not os.path.exists(d_name):
        return jsonify({"json_conf": json_conf})

    for root, _, files in os.walk(d_name):
        for filename in files:
            try:
                with open(os.path.join(root, filename), 'r') as load_f:
                    json_conf[filename] = json.load(load_f)
            except Exception as e:
                pass

    return jsonify({"json_conf": json_conf})


@app.route("/replace_minio_dir", methods=["POST", "GET"])
def ReplaceMinioDir():
    try:
        pid = None

        if request.form.get('pid', None):
            pid = request.form.get('pid', None)
        f = request.files['casefile.zip']

        print('%s   %s' % (pid, f.filename))
        if not pid:
            return jsonify({"ret": -1, "err": "pid not current"})
        
        tmpfile = tempfile.NamedTemporaryFile()
        f.save(tmpfile.name)
        print(tmpfile.name)

        d_name = '/home/data/' + pid
        if os.path.exists(d_name):
            shutil.rmtree(d_name)

            unziptmp = tempfile.mkdtemp()
            with zipfile.ZipFile(tmpfile.name, "r") as zf:
                zf.extractall(unziptmp)

            shutil.move(unziptmp, d_name)

        d_z_name = '/home/data/' + pid + '-zip'
        if os.path.exists(d_z_name):
            shutil.rmtree(d_z_name)
    except Exception as e:
        print(str(e))
        return jsonify({"ret": -1, "err": str(e)})

    return jsonify({"ret": 0, "err": "ok"})

@app.route("/git/repalce_minio_dir", methods=["POST"])
def git_replace_minio_dir():
    pass

@app.route("/create_project_casefile", methods=["POST", "GET"])
def CreateProjectCasefile():
    try:
        pid = None

        if request.form.get('pid', None):
            pid = request.form.get('pid', None)
        f = request.files['casefile.zip']

        print('%s   %s' % (pid, f.filename))
        if not pid:
            return jsonify({"ret": -1, "err": "pid not current"})

        tmpfile = tempfile.NamedTemporaryFile()
        f.save(tmpfile.name)
        print(tmpfile.name)

        print('11111')
        
        d_name = '/home/data/' + pid
        if os.path.exists(d_name):
            shutil.rmtree(d_name)

        print('222222')
        unziptmp = tempfile.mkdtemp()
        with zipfile.ZipFile(tmpfile.name, "r") as zf:
            zf.extractall(unziptmp)

        shutil.move(unziptmp, d_name)

    except Exception as e:
        print(str(e))
        return jsonify({"ret": -1, "err": str(e)})

    return jsonify({"ret": 0, "err": "ok"})

@app.route("/copy_project_case", methods=["POST", "GET"])
def CopyProjectCase():
    try:
        source_directory = None
        target_directory = None
        if request.form.get('source_directory', None):
            source_directory = request.form.get('source_directory', None)
        if request.form.get('target_directory', None):
            target_directory = request.form.get('target_directory', None)

        if not source_directory or not target_directory:
            return jsonify({"ret": -1, "err": " source_directory and target_directory not allow None"})


        if len(source_directory) != 8 or len(target_directory) != 8:
            return jsonify({"ret": -1, "err": "source_directory and target_directory are not right"})

        s_directory = '/home/data/%s' % source_directory
        t_directory = '/home/data/%s' % target_directory

        shutil.copytree(s_directory, t_directory)

    except Exception as e:
        return jsonify({"ret": -1, "err": str(e)})

    return jsonify({"ret": 0, "err": "ok"})

def main():

    app.run(host="0.0.0.0", port=4000)

if __name__ == "__main__":
    
    main()
