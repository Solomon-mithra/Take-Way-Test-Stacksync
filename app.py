from flask import Flask, request, jsonify
import sys
import io

import tempfile
import subprocess
import os
import json

app = Flask(__name__)


@app.route('/execute', methods=['POST'])
def execute_script():
    if request.content_type != "text/plain":
        return jsonify({"error": "Content-Type must be text/plain"}), 400

    try:
        script = request.data.decode("utf-8")
    except Exception as e:
        return jsonify({"error": f"Script decoding failed: {str(e)}"}), 400

    if "def main" not in script:
        return jsonify({"error": "main() function not found"}), 400

    # Save to temporary file
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write(script + "\n\nif __name__ == '__main__':\n    import json; print(json.dumps(main()))")
        script_path = f.name

    try:
        result = subprocess.run([
            "nsjail",
            "--quiet",
            "--disable_proc",
            "--disable_clone_newnet",
            "--rlimit_as", "512",              # 512MB memory limit
            "--time_limit", "5",               # 5 seconds CPU time
            "--chroot", "/",                   # root jail
            "--user", "99999",
            "--group", "99999",
            "--", "python3", script_path
        ], capture_output=True, text=True, timeout=5)

        if result.returncode != 0:
            raise Exception(result.stderr.strip() or "Script failed in jail")

        return jsonify({
            "result": json.loads(result.stdout.strip()),
            "stdout": result.stdout
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        os.remove(script_path)

if __name__ == "__main__":
    app.run(port=8080, debug=True)
