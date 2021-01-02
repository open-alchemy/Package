var dynalite = require("dynalite");
var dynaliteServer = dynalite({ createTableMs: 0 });

// Listen on port 8000
dynaliteServer.listen(8000, function (err) {
  if (err) throw err;
  console.log("Dynalite started on port 8000");
});
