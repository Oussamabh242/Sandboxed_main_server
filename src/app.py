
from flask import Flask, jsonify, request
import requests
from . import utils
from .db import db, init_db, Problem
import json
from flask_cors import CORS 
from flask_swagger_ui import get_swaggerui_blueprint

submit = "http://127.0.0.1:3000/submit"
run = "http://127.0.0.1:3000/run"
problemCreate = "http://127.0.0.1:3000/problem"

SWAGGER_URL = "/swagger" 
API_URL = "/static/swagger.json" 
swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config = {
        'app_name': 'Access API'
    }
)

app = Flask(__name__)
app.register_blueprint(swagger_ui_blueprint , url_prefix = SWAGGER_URL)
CORS(app) 
init_db(app)



@app.route("/code/submit", methods=['POST'])
def submit_code():
    try:
        data = request.json
        check_result = utils.check_req_data(data, ["code", "language", "problemId"])
        if not check_result:
            return jsonify({"error": "missing values"}), 400
        x = requests.post(submit, json=data)
        return jsonify(x.json()), x.status_code
    except Exception as err:
        return jsonify({"err": str(err)}), 500

@app.route("/code/run", methods=['POST'])
def run_code():
    try:
        data = request.json
        check_result = utils.check_req_data(data, ["code", "language", "problemId"])
        if not check_result:
            return jsonify({"error": "missing values"}), 400
        x = requests.post(run, json=data)
        return jsonify(x.json()), x.status_code
    except Exception as err:
        return jsonify({"err": str(err)}), 500

@app.route("/problem", methods=["POST", "GET"])
def problems():
    if request.method == "POST" : 
        try:
            data = request.json
            print(data)
            problem = Problem(
                title=data.get("title"),
                description=data.get("description"),
                constraints=data.get("constraints"),  
                difficulty=data.get("difficulty", "Easy") ,
                templates = json.dumps(data.get("templates"))
            )
            db.session.add(problem)
            db.session.flush() 
            sandbox_req = {
            "id" :problem.id ,
            "testCases" : data["testCases"],
            "order": data["order"],
            "functionName" :data["functionName"],
            "execTime": data["execTime"]
            }

            sandbox_res = requests.post(problemCreate , json=sandbox_req) ; 
            if sandbox_res.status_code == 201 : 
                db.session.commit()
                return jsonify({"message": "Problem created successfully", "problem_id": problem.id}), 201
            else: 
                db.session.rollback()
                return jsonify({"error": "Failed to create problem in sandbox"}), sandbox_res.status_code
            
        except Exception as err:
            print(err)
            db.session.rollback()
            return jsonify({"error": "Something went wrong"}), 500
    
    elif request.method == "GET" : 
        try : 
            problems_req = db.session.execute(db.select(Problem)).scalars()
            problems_req = [problem.to_dict() for problem in problems_req]
            return jsonify(problems_req) 
        except Exception as e : 
            print(e) 
            return jsonify({"error" :  "error happend"}) , 500

@app.route("/problem/<problemId>", methods = ["GET"])
def fetch_problem(problemId) : 
    try : 
        problem = db.session.execute(db.select(Problem).filter_by(id = problemId)).scalar_one().to_dict()
        return jsonify(problem) 
    except Exception as e : 
        print(e) 
        return jsonify({"error" , "error happend"}) , 500



if __name__ == "__main__":
    app.run(debug=True)








