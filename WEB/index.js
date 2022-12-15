const express = require('express');
const app = express();
const ejs = require('ejs');
const YAML = require('yamljs');
const fs = require("fs");
app.engine('html', ejs.__express);
app.set('view engine', 'html');

app.get("/",(req,res)=>{
    res.render('index.html', { title: 'DisCloudDisk' });
})


app.get("/setting",(req,res)=>{
    console.log("setting:",req.query.data)
    data = req.query.data;
    data = JSON.parse(atob(data))
    res.send(data);
})

app.get("/load",(req,res)=>{
    console.log("setting  request")
    var data = YAML.parse(fs.readFileSync("../config.yaml").toString());
    res.send(data);
})


app.listen(81, () => {
    console.log('running at http://127.0.0.1');
})


