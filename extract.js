const fs = require('fs');
const content = fs.readFileSync('index.html', 'utf8');
const scriptMatch = content.match(/<script type="text\/babel">([\s\S]*?)<\/script>/);

if (scriptMatch) {
    const babelCode = scriptMatch[1];
    fs.writeFileSync('temp.jsx', babelCode);
    console.log("Successfully wrote temp.jsx.");
} else {
    console.error("Could not find babel script.");
}
