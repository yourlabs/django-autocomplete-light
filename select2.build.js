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
        let code = `var dalLoadLanguage = function (jQuery) { 
            ${fs.readFileSync(file.path, "utf8")} 
        } 
        var event = new CustomEvent("dal-language-loaded", { lang: "${file.file.slice(0, -3)}"});
        document.dispatchEvent(event);`;
        let inputs = {};
        inputs[file.file] = code;
        let result = UglifyJS.minify(inputs, {output: {}})
        fs.writeFile(`src/dal/static/autocomplete_light/i18n/${file.file}`, result.code, (err => {
            if (err) throw err;
        }))
    });
});

const concat = require('concat');

let inputs = [
    'src/dal/static/autocomplete_light/jquery.init.js',
    'node_modules/select2/dist/js/select2.full.js',
    'src/dal/static/autocomplete_light/autocomplete.init.js',
    'src/dal/static/autocomplete_light/forward.js',
    'src/dal/static/autocomplete_light/select2.js',
    'src/dal/static/autocomplete_light/jquery.post-setup.js',
];

concat(inputs, 'src/dal/static/autocomplete_light/autocomplete.js');