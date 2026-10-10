const { spawn } = require('child_process');
const fs = require('fs');

const py = 'C:\\Users\\YX\\.dsh\\dsh-runtimes\\dsh-primary-runtime\\dependencies\\python\\python.exe';
const script = 'F:\\Projects\\JavaInterview\\run_extract.py';

const p = spawn(py, [script], { stdio: 'inherit' });
p.on('close', (code) => {
  fs.writeFileSync('F:\\Projects\\JavaInterview\\node_done.txt', 'Done with code ' + code);
});
