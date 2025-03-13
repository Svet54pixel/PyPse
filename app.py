from flask import Flask, request, render_template, jsonify, send_file
import subprocess
from subprocess import PIPE, check_output
import os
import sys, io
from pypse import shell
from pypse import pypse_run 
app = Flask(__name__)

@app.route('/')
def index():
    return send_file('index.html')

@app.route("/compile", methods=['POST'])
def compilePs():
    pseu = request.json.get('pseudocode')
    if not pseu:
        return jsonify({"error": "No pseudocode provided"}), 400
    def getSValue(x):
        length = len(pseu)
    a = True
    error1 = False
    while a:
        b = pseu.find("INTEGER")
        if b == -1:
            a = False
        else:
            pseu = pseu[0:b] + "INT" + pseu[b+7:]
    a = True
    while a:
        b = pseu.find("BOOLEAN")
        if b == -1:
            a = False
        else:
            pseu = pseu[0:b] + "BOOL" + pseu[b+7:]
    a = True
    while a:
        b = pseu.find("CHAR")
        if b == -1:
            a = False
        else:
            pseu = pseu[0:b] + "STRING" + pseu[b+4:]
    a = True
    m = 0
    flag = True
    #try except structure here
    while a and flag:
        temporary = pseu[m:]
        b =  temporary.find("FOR")


        if b == -1:
            a = False
        else:
            c  = 3
            rep = ""
            while temporary[ b + c] == " ":
                c = c+1
                
            while temporary[b+c] != " " and temporary[b+c] != "<":
                
                rep = rep + temporary[b+c]
                
                c = c+1
            d = temporary.find("NEXT")
            error1 = False
            if d == -1:
                error1 = True
                flag = False
            else:
                while temporary[d+4] == " ":
                    temporary = temporary[:d+4] + temporary[d+5:]
                    
            g = "NEXT" + rep
            d = temporary.find(g)
            if d == -1:
                error1 = True
                flag = False
            else:
                d = d + m  #location in temporary + start of temporary in original file
                m = d + len(g)+1
                
                pseu = pseu[:d] + "ENDFOR" + pseu[m:]
                m = d + 6
                
    try:
        sys.stdout = io.StringIO()
        sys.stderr = io.StringIO()
        temp_filename = "temp.pse"
        with open(temp_filename, "w") as f:
            f.write(pseu)
        file = open(temp_filename, "r")
        options = {}
        #options["name"] = "temp.pse"
        options['file'] = file
        pypse_run.pypse_run(**options)
        output = sys.stdout.getvalue()
        sys.stout = sys.__stdout__
        error = sys.stderr.getvalue()
        sys.stderr = sys.__stderr__
        if error1:
            error = "Missing the end of the For statement (should close with NEXT <variable>)"
        if error == "":
            output = output[:-16]
            while output[0:3] != "...":
                output = output[1:]
            output = output[3:]
        elif output != "":
            while output[0:3] != "...":
                output = output[1:]
            output = output[3:]
        if error.find("AttributeError: 'NoneType'") != -1:
           error = "Declaration is missing or incorrect for one of the variables"
        if error.find("lark.exceptions.UnexpectedCharacters: No terminal matches") != -1:
            start = error.find("lark.exceptions.UnexpectedCharacters: No terminal matches") + len("lark.exceptions.UnexpectedCharacters: No terminal matches")
            error = error[start:]
            if error.find("lark.exceptions.UnexpectedCharacters: No terminal matches ',' in the current parser context,") != -1:
                error = error + "Compiler does not accept more than one declarations per line though it is not wrong by sylabus. So declarations must follow the style of : DECLARE <variable> : <DataType>" & error
        if error.find("TypeError:") != -1:
            a = error.find("TypeError:")
            error = error[a:] + "Try checking if you did not initialize a variable"

        # if os.path.exists(temp_filename):
        #     os.remove(temp_filename)
        return jsonify({"output": output, "error": error})
    except Exception as e:
        return jsonify({"error": str(e)}), 500     
    



@app.route("/compile2", methods=['POST'])
def compilePs2():
    pseu = request.json.get("pseudocode2")
    if not pseu:
        return jsonify({"error": "No pseudocode provided"}), 400
    
    a = True
    error1 = False
    while a:
        b = pseu.find("INTEGER")
        if b == -1:
            a = False
        else:
            pseu = pseu[0:b] + "INT" + pseu[b+7:]
    a = True
    while a:
        b = pseu.find("BOOLEAN")
        if b == -1:
            a = False
        else:
            pseu = pseu[0:b] + "BOOL" + pseu[b+7:]
    a = True
    while a:
        b = pseu.find("CHAR")
        if b == -1:
            a = False
        else:
            pseu = pseu[0:b] + "STRING" + pseu[b+4:]
    a = True
    m = 0
    flag = True
    #try except structure here
    while a and flag:
        print("loop1")
        temporary = pseu[m:]
        b =  temporary.find("FOR")
        print(temporary)
        if b == -1:
            a = False
        else:
            c  = 3
            rep = ""
            while temporary[ b + c] == " ":
                c = c+1
                print("loop2")
            while temporary[b+c] != " " and temporary[b+c] != "<":
                print(temporary[b+c])
                rep = rep + temporary[b+c]
                print("loop3")
                c = c+1
            d = temporary.find("NEXT")
            error1 = False
            if d == -1:
                error1 = True
                flag = False
            else:
                while temporary[d+4] == " ":
                    temporary = temporary[:d+4] + temporary[d+5:]
                    print("loop4")
            g = "NEXT" + rep
            d = temporary.find(g)
            if d == -1:
                error1 = True
                flag = False
            else:
                d = d + m  #location in temporary + start of temporary in original file
                m = d + len(g)+1
                pseu = pseu[:d] + "ENDFOR" + pseu[m:]
                m = d + 6  
    try:
        sys.stdout = io.StringIO()
        sys.stderr = io.StringIO()
        temp_filename = "temp.pse"
        with open(temp_filename, "w") as f:
            f.write(pseu)
        file = open(temp_filename, "r")
        options = {}
        #options["name"] = "temp.pse"
        options['file'] = file
        pypse_run.pypse_run(**options)
        output = sys.stdout.getvalue()
        sys.stout = sys.__stdout__
        error = sys.stderr.getvalue()
        sys.stderr = sys.__stderr__
        # output = result.stdout
        # # output = output + pypse_run.pypse_run(**options)
        # error = result.stderrr
        if error1:
            error = "Missing the end of the For statement (should close with NEXT <variable>)"
        if error == "":
            output = output[:-16]
            while output[0:3] != "...":
                output = output[1:]
            output = output[3:]
        elif output != "":
            while output[0:3] != "...":
                output = output[1:]
            output = output[3:]
        if error.find("AttributeError: 'NoneType'") != -1:
            error = "Declaration is missing or incorrect for one of the variables"
        if error.find("lark.exceptions.UnexpectedCharacters: No terminal matches") != -1:
            start = error.find("lark.exceptions.UnexpectedCharacters: No terminal matches") + len("lark.exceptions.UnexpectedCharacters: No terminal matches")
            error = error[start:]
            if error.find("lark.exceptions.UnexpectedCharacters: No terminal matches ',' in the current parser context,") != -1:
                error = error + "Compiler does not accept more than one declarations per line though it is not wrong by sylabus. So declarations must follow the style of : DECLARE <variable> : <DataType>" & error
        if error.find("TypeError:") != -1:
            a = error.find("TypeError:")
            error = error[a:] + "Try checking if you did not initialize a variable"

        # if os.path.exists(temp_filename):
        #     os.remove(temp_filename)
        return jsonify({"output2": output, "error2": error})
    except Exception as e:
        return jsonify({"error2": str(e)}), 500



@app.route("/compile3", methods=['POST'])
def compilePs3():
    pseu = request.json.get("pseudocode3")
    pseu = "DECLARE FNString : STRING " + "FNString <- \"Hi Hello I Am A Dictionary Me \"" + pseu
    if not pseu:
        return jsonify({"error": "No pseudocode provided"}), 400
    
    a = True
    error1 = False
    while a:
        b = pseu.find("INTEGER")
        if b == -1:
            a = False
        else:
            pseu = pseu[0:b] + "INT" + pseu[b+7:]
    a = True
    while a:
        b = pseu.find("BOOLEAN")
        if b == -1:
            a = False
        else:
            pseu = pseu[0:b] + "BOOL" + pseu[b+7:]
    a = True
    a = True
    while a:
        b = pseu.find("CHAR")
        if b == -1:
            a = False
        else:
            pseu = pseu[0:b] + "STRING" + pseu[b+4:]
    a = True
    m = 0
    flag = True
    #try except structure here
    while a and flag:
        print("loop1")
        temporary = pseu[m:]
        b =  temporary.find("FOR")
        print(temporary)
        if b == -1:
            a = False
        else:
            c  = 3
            rep = ""
            while temporary[ b + c] == " ":
                c = c+1
                print("loop2")
            while temporary[b+c] != " " and temporary[b+c] != "<":
                print(temporary[b+c])
                rep = rep + temporary[b+c]
                print("loop3")
                c = c+1
            d = temporary.find("NEXT")
            error1 = False
            if d == -1:
                error1 = True
                flag = False
            else:
                while temporary[d+4] == " ":
                    temporary = temporary[:d+4] + temporary[d+5:]
                    print("loop4")
            g = "NEXT" + rep
            d = temporary.find(g)
            if d == -1:
                error1 = True
                flag = False
            else:
                d = d + m  #location in temporary + start of temporary in original file
                m = d + len(g)+1
                pseu = pseu[:d] + "ENDFOR" + pseu[m:]
                m = d + 6
            
    try:
        sys.stdout = io.StringIO()
        sys.stderr = io.StringIO()
        temp_filename = "temp.pse"
        with open(temp_filename, "w") as f:
            f.write(pseu)
        file = open(temp_filename, "r")
        options = {}
        #options["name"] = "temp.pse"
        options['file'] = file
        pypse_run.pypse_run(**options)
        output = sys.stdout.getvalue()
        sys.stout = sys.__stdout__
        error = sys.stderr.getvalue()
        sys.stderr = sys.__stderr__
        if error1:
            error = "Missing the end of the For statement (should close with NEXT <variable>)"
        if error == "":
            output = output[:-16]
            while output[0:3] != "...":
                output = output[1:]
            output = output[3:]
        elif output != "":
            while output[0:3] != "...":
                output = output[1:]
            output = output[3:]
        if error.find("AttributeError: 'NoneType'") != -1:
            error = "Declaration is missing or incorrect for one of the variables"
        if error.find("lark.exceptions.UnexpectedCharacters: No terminal matches") != -1:
            start = error.find("lark.exceptions.UnexpectedCharacters: No terminal matches") + len("lark.exceptions.UnexpectedCharacters: No terminal matches")
            error = error[start:]
            if error.find("lark.exceptions.UnexpectedCharacters: No terminal matches ',' in the current parser context,") != -1:
                error = error + "Compiler does not accept more than one declarations per line though it is not wrong by sylabus. So declarations must follow the style of : DECLARE <variable> : <DataType>" & error
        if error.find("TypeError:") != -1:
            a = error.find("TypeError:")
            error = error[a:] + "Try checking if you did not initialize a variable"

        # if os.path.exists(temp_filename):
        #     os.remove(temp_filename)
        return jsonify({"output3": output, "error3": error})

    except Exception as e:
        return jsonify({"error3": str(e)}), 500




# def index():
#     text = request.form.get('textarea')
#     print(text)
#     return(text) 
if __name__ == '__main__':
    app.run()