/*
 * Pull all JS files into single file.
 */

//requiring path and fs modules
const path = require('path');
const fs = require('fs');
const UglifyJS = require('uglify-js');

// Gather list of translation files
const directoryPath = path.join(__dirname, 'node_modules/select2/dist/js/i18n');

function getLanguageFiles(cb) {
    fs.readdir(directoryPath, function (err, files) {
        if (err) {
            return console.log('Unable to scan directory: ' + err);
        }
        let fileArray = [];
        files.forEach(function (file) {
            if (file.endsWith('.js')) {
                fileArray.push({file: file, path: path.join(directoryPath, file)})
            }
        });
        cb(fileArray);
    });
}

getLanguageFiles(function (files) {
    files.forEach(function (file) {
        let license, contents;
        [license, ...contents] = fs.readFileSync(file.path, "utf8").split('\n');
        let code = `${license}
        
        var dalLoadLanguage = function (jQuery) { 
            ${contents.join('')} 
        } 
        var event = new CustomEvent("dal-language-loaded", { lang: "${file.file.slice(0, -3)}"});
        document.dispatchEvent(event);`;
        let inputs = {};
        inputs[file.file] = code;
        let result = UglifyJS.minify(inputs, {output: {comments: true}})
        fs.writeFile(`src/dal/static/autocomplete_light/i18n/${file.file}`, result.code, (err => {
            if (err) throw err;
        }))
    });
});