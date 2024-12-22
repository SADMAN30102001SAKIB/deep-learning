const { exec } = require('child_process');

const array = [2, 1, 8, 4].join(' ');

exec(`python test.py ${array}`, (error, stdout, stderr) => {
  if (error) {
    console.error(`Error: ${error.message}`);
    return;
  }
  if (stderr) {
    console.error(`Stderr: ${stderr}`);
    return;
  }
  console.log(`Output: ${stdout}`);
});
