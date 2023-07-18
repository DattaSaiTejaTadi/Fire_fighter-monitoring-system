var mysql=require('mysql');
var mysqlcon=mysql.createConnection({
  host:'localhost',
  database:'project',
  user:'root',
  password:'password'
})
mysqlcon.connect((err)=>{
  if(err){
    console.log(err);
    console.log("error occurred");
  }
  else{
    console.log("connection created");
  }
})
module.exports=mysqlcon;
