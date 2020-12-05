var dynalite = require('dynalite')
var dynaliteServer = dynalite({ path: './tests/library/facades/database/test-db', createTableMs: 0 })

// Listen on port 8000
dynaliteServer.listen(8000, function(err) {
  if (err) throw err
  console.log('Dynalite started on port 8000')
})
