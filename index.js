const express = require('express')
const { spawn } = require('child_process')
const fs = require("fs")
const app = express()
var cors = require('cors');
app.use(cors());
const port = 5000
app.get('/search', (req, res) => {

    var id = req.query.id;

    // let id = req.query.keyword;
    console.log(id);
    var dataToSend;
    // spawn new child process to call the python script
    const python = spawn('python', ['ranking_algo_and_main.py', id]);


    // collect data from script
    python.stdout.on('data', function (data) {
        console.log('Pipe data from python script ...');
        dataToSend = data.toString();
    });

    // in close event we are sure that stream from child process is closed

    python.on('close', (code) => {
        console.log(`child process close all stdio with code ${code}`);
        // send data to browser
       
        //  res.send(dataToSend)

        const rStream = fs.createReadStream("final_products.json");
        rStream.pipe(res);

    });

})

app.get('/ranking', (req, res) => {
    const rStream = fs.createReadStream("rank_list.json");
    rStream.pipe(res);
})
app.listen(port, () => console.log(`Example app listening on port 
${port}!`))