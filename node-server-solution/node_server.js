const express = require('express');
const { exec } = require('child_process');
const bodyParser = require('body-parser');

const app = express();
const port = 3001;

app.use(bodyParser.json());

// Enable CORS
app.use((req, res, next) => {
  res.header('Access-Control-Allow-Origin', '*');
  res.header('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept');
  next();
});

app.post('/answer-question', (req, res) => {
  const { question } = req.body;

  // Replace 'python_script.py' with the path to your Python script.
  const pythonScriptPath = 'app.py';

  // Construct the command to run the Python script with arguments.
  const command = `python ${pythonScriptPath} "${question}"`;

  // Execute the Python script from Node.js
  exec(command, (error, stdout, stderr) => {
    if (error) {
      console.error(`Error executing Python script: ${error}`);
      res.status(500).json({ error: 'Error executing Python script' });
      return;
    }

    // Parse the Python script's output
    let pythonResult;
    try {
      pythonResult = JSON.parse(stdout);
    } catch (e) {
      console.error('Error parsing Python result:', e);
      res.status(500).json({ error: 'Error parsing Python result' });
      return;
    }

    // Use the result in your Node.js application
    console.log('Received Python result:', pythonResult);
    res.json({ pythonResult });
  });
});

app.listen(port, () => {
  console.log(`Node.js server is running at http://localhost:${port}`);
});
