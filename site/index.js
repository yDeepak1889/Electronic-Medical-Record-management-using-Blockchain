const express        = require('express');
const router           = express.Router();
const app            = express();

var port = process.env.PORT || 3000;

var server = app.listen(port, function() {
	console.log('Express server listening on port ' + port);
});

app.use('/test', router);

router.get('/uploadNewData', function(req, res) {
	var dir = __dirname;
	res.sendFile(dir + '/uploadNewData.html');
});