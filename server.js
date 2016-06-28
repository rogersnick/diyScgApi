var express = require('express');
var app = express();
var PythonShell = require('python-shell');



var router = express.Router();
var port    = 	process.env.PORT || 9090;

router.get('/', function(req, res) {
  res.send('hello world');
});

router.get('/json/:card', function(req, res) {

    args = [req.params.card];
    var pyshell = new PythonShell('cut_img.py',{args: args});


    pyshell.on('message', function (message) {
      // received a message sent from the Python script (a simple "print" statement)
      res.status("200").send(message);
    });

    // end the input stream and allow the process to exit
    pyshell.end(function (err) {
      if (err) throw err;
    });


});


// apply the routes to our application
app.use('/', router);

app.listen(port);
console.log('Magic happens on port ' + port);
