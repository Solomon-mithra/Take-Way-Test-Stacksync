from flask import Flask, request, jsonify
import sys
import io

import tempfile
import subprocess
import os
import json

app = Flask(__name__)


def run_script_with_nsjail(script_code):
    project_root = os.path.abspath(os.path.dirname(__file__))
    script_path = os.path.join(project_root, "user_script.py")
    with open(script_path, "w") as f:
        f.write(script_code)
        f.write('\n\nif __name__ == "__main__":\n')
        f.write('    import json\n')
        f.write('    result = main()\n')
        f.write('    print("___RESULT_START___")\n')
        f.write('    print(json.dumps(result))\n')
        f.write('    print("___RESULT_END___")\n')
    cmd = [
        os.path.abspath("./nsjail_bin"),
        "-Mo",
        "--chroot", "/",
        "--mount", "none:/app:tmpfs:size=10M",
        "--bindmount_ro", f"{project_root}:/app",
        "--cwd", "/app",
        "--", "/app/takeAwayTest/bin/python3", "user_script.py"
    ]
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=10)
    stdout = proc.stdout.decode()
    stderr = proc.stderr.decode()
    # Extract result from stdout
    result = None
    out_lines = []
    in_result = False
    for line in stdout.splitlines():
        if line.strip() == "___RESULT_START___":
            in_result = True
            continue
        if line.strip() == "___RESULT_END___":
            in_result = False
            continue
        if in_result:
            try:
                result = json.loads(line)
            except Exception:
                return None, stdout, stderr, 'main() did not return valid JSON'
        else:
            out_lines.append(line)
    if result is None:
        return None, stdout, stderr, 'main() did not return a result'
    # Clean up the script file
    os.remove(script_path)
    return result, '\n'.join(out_lines), None, None


@app.route('/execute', methods=['POST'])
def execute():
    data = request.get_json()
    if not data or 'script' not in data:
        return jsonify({'error': 'Missing script field'}), 400
    script = data['script']
    if 'def main' not in script:
        return jsonify({'error': 'No main() function found'}), 400
    result, stdout, _, err = run_script_with_nsjail(script)
    if err:
        return jsonify({'error': err, 'stdout': stdout}), 400
    return jsonify({'result': result, 'stdout': stdout})


if __name__ == "__main__":
    app.run(port=8080, debug=True)
