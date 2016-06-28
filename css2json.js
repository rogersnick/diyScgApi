
// converts css to an AST object. prints that object
// run as node css2json.js filename
var http = require('http');
var fs = require('fs');
var css = require('css');
fileName = process.argv[2];

//file = fs.open(fileurl,'r');



(function() {
  var fileName = process.argv;
  if ( Array.isArray(fileName) ) {

    // Assign obj to third CLI command
    var filePath = process.argv[2];
    var newFile = filePath.replace('css', 'json');

    fs.readFile(filePath, 'utf8', function(err, data) {
      if (err) {
        return console.log('Error: ' + err);
      }

      if (data) {
        //console.log(data);
       	obj = css.parse(data);
       	ret = css.parse(css.stringify(obj));
       	console.log('%j', ret);

      }
    });

  } else {
    return console.log( 'Failsauce ');
  }
})();
