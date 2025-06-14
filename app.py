from flask import Flask, request, jsonify
import sys
import io

app = Flask(__name__)

@app.route('/execute', methods=['POST'])
def execute_script():
    data = request.get_json()
    raw_script = data.get("script", "")

    # Convert escaped newlines and tabs to real ones
    try:
        script = bytes(raw_script, "utf-8").decode("unicode_escape")
    except Exception as e:
        return jsonify({"error": f"Invalid script encoding: {str(e)}"}), 400

    if "def main" not in script:
        return jsonify({"error": "main() function not found"}), 400

    # Capture stdout
    captured_output = io.StringIO()
    sys_stdout_backup = sys.stdout
    sys.stdout = captured_output

    try:
        local_vars = {}
        exec(script, {}, local_vars)
        if "main" not in local_vars:
            return jsonify({"error": "main() not defined"}), 400

        result = local_vars["main"]()
        return jsonify({
            "result": result,
            "stdout": captured_output.getvalue()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        sys.stdout = sys_stdout_backup

if __name__ == "__main__":
    app.run(port=8080, debug=True)
