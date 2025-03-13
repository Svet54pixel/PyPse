# from flask import Flask, request, render_template, jsonify, send_file
# import subprocess
# from subprocess import PIPE, check_output
# import os
# from pypse import shell
# from pypse import pypse_run 
# app = Flask(__name__)
# temp_filename = "temp.pse"
# file = open(temp_filename, "r")
# options = {}
# #options["name"] = "temp.pse"
# options['file'] = file
# def a():
#     result = subprocess.run(
#             pypse_run.pypse_run(**options),
#             stdout=subprocess.PIPE,
#             stderr=subprocess.PIPE,
#             shell=True,
#             text=True
#         )
#     return result