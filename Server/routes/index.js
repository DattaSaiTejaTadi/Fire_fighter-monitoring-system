var express = require('express');
const session = require('express-session');
var router = express.Router();
var con=require("./sql");
const accountSid = 'ACdacf8b9b01a8457897f793a8b67c17e6';
const authToken = '1baeaebaa817d54ee661d5addc8304ea';
const client = require('twilio')(accountSid, authToken);



//render files
router.get('/admin',(req,res)=>{
  res.render('admin');
});

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { title: 'Express' });
});
router.get('/login-page',(req,res)=>{
  res.render('login-page')
})
router.get('/mai',(req,res)=>{
  res.render('mai');
});

router.get('/home',(req,res)=>{
  res.render('home');
});

//website data
// polling status to firefighters
router.get('/status', (req, res) => {
  con.query('SELECT * FROM location WHERE district='+'"'+req.session.fire_fighter.district+'"', (error, rows) => {
    if (error) {
      console.log(error)
      return res.sendStatus(500);
    }
    
    res.send(rows);
  });
});
router.get('/userdata',(req,res)=>{
  con.query(`select * from fire_fighter where id="${req.session.fire_fighter.id}"`,(err,rows)=>{
    if(!err){
      console.log(rows[0]);
      res.send(rows[0]);
    }else{
      console.log(err);
    }
  })
});

router.get('/firefighterRegister',(req,res)=>{
  if(req.session.fire_fighter.role=='driver engineer' ||req.session.fire_fighter.role=='Chief'){
    res.render('register');
  }else{
    res.send('only driver engineers can access');
  }
  
});

router.post('/firefighterRegister',(req,res)=>{
  var quer=`insert into fire_fighter(id,name,phone,address,station,role,password,district) values("${req.body.id}","${req.body.name}","+91${req.body.phone}","${req.body.address}","${req.body.station}","${req.body.role}","${req.body.password}","${req.body.district}")`;
  con.query(quer,(err,rows)=>{
    if(!err){
      res.redirect('/firefighterRegister');
    }else{
      console.log(err);
      res.send("cant register");
    }
  })
});

router.post('/login',(req,res)=>{
  console.log(req.body.id+" "+req.body.password)
  
  var que='select * from fire_fighter where id='+'"'+req.body.id+'"'+'and password='+'"'+req.body.password+'"';
  console.log(que)

  // Query the database to check if the user exists
  con.query(que, (error, results) => {
    if (error) {
      console.log(error);
    }

    // If the user exists, create a session
    if (results.length) {
      req.session.fire_fighter = results[0];
      return res.redirect('/home');
    }

    // Otherwise, show an error message
     res.redirect('/')
  });
});
router.get('/logout', (req, res)=>{
  req.session.destroy(err => {
      if(err){
          return res.redirect('/mai')
      }
      res.clearCookie()
      res.redirect('/')
  })
});
//firepost
router.post('/firepost',(req,res)=>{
  con.query('update location set status="fire" where location_id='+req.body.location_id,(err,rows)=>{
    con.query(`select * from fire_fighter where district="${req.body.district}"`, (err3,row3)=>{
      if(!err3){
        for(var obj1 of row3){
          console.log("i got here")
          console.log(obj1.phone)
          client.calls.create({
          twiml: '<Response><Say >fire has generated ,please perform your duty, for location details please check message</Say></Response>',
         to: obj1.phone,
         from: '+12183955753'
          })
          .then(call => console.log(call.status))
          .catch(error=>console.log(error));
        }
      }
      else{
        console.log(err3);
      }
    })
    con.query(`select * from fire_fighter where district="${req.body.district}"`, (err4,row4)=>{
      if(!err4){
        for(var obj3 of row4){
          console.log(obj3.phone);
          client.messages.create({
            body:`Fire at Location id : ${req.body.location_id} \nAddress : ${req.body.address_line}\n Pincode : ${req.body.pincode}\n District : ${req.body.district}\n State: ${req.body.state}`,
            to:obj3.phone,
            from: '+12183955753'
          })
          .then(message => console.log(message.status))
          .catch(error=>console.log(error));
    
        }
      }
      else{
        console.log(err3);
      }
    })
   
    con.query('select * from people where location_id='+req.body.location_id,(err,rows2)=>{
      if(!err){
        for(var obj of rows2){
          console.log(obj.phone);
          client.calls.create({
         twiml: '<Response><Say >Please be cautious , your surroundings on fire   </Say></Response>',
         to: obj.phone,
         from: '+12183955753'
       })
      .then(call => console.log(call.status))
      .catch(error=>console.log(error));
        }
      }
    }
    )
    if(err){
      console.log(err)
    }
    else{
      res.sendStatus(200)
    }
  }
  );
}
);
router.post('/maintain',(req,res)=>{
  con.query('update location set report='+'"'+req.session.fire_fighter.id+'"'+', status="under_maintainance" , time=current_timestamp  where location_id='+req.body.location_id,(err,rows)=>{
    if(err){
      console.log(err)
    }else{
      res.sendStatus(200);
    }
  })
});
router.post('/finish',(req,res)=>{
  con.query('update location set status="under_control",time=current_timestamp where location_id='+req.body.location_id,(err,rows)=>{
    if(err){
      console.log(err);
    }else{
      res.sendStatus(200);
    }

  })
});
// application api's
// handshake for application
router.get('/handsake',(req,res)=>{
  con.query("select location_id from location",(err,rows,fields)=>{
    if(!err){
      res.send(rows);
    }
    else{
      console.log(err);
    }
  })
});
// registeration for location
router.post('/register',(req,res)=>{
  console.log(req.body);
  con.query('insert into location(address_line,pincode,district,state,location_id,time,status,city) values ('+'"'+req.body.address_line+'"'+','+req.body.pincode+','+'"'+req.body.district+'"'+','+'"'+req.body.state+'"'+','+req.body.location_id+','+'current_timestamp'+','+'"under_control"'+','+'"'+req.body.city+'"'+')',(err,rows,fields)=>{
    if(!err){
      res.sendStatus(200);
    }
    else{
      console.log(err)
      res.sendStatus(500);
    }
  })
});
// people registering

router.post('/registerpeople',(req,res)=>{
  var lis=req.body;
  console.log(lis);
  for(var obj of lis){
    var squery='insert into people(name,phone,location_id) values ('+'"'+obj.name+'"'+','+'"+91'+obj.phone+'"'+','+obj.location_id+')';
    console.log(squery);
    con.query(squery,(err,rows,fields)=>{
      if(err){
        flag=0;
      }
    })
  }
  res.sendStatus(200);
})

//getuser
router.post('/getusers',(req,res)=>{
  con.query('select * from people where location_id='+req.body.location_id,(err,rows)=>{
    if(err){
      console.log(err)
    }
    else{
      console.log(rows);
      res.send(rows)
    }
  })
});

router.get('/getlocations',(req,res)=>{
  con.query("select * from location",(err,rows,fields)=>{
    if(!err){
      res.send(rows);
    }
    else{
      console.log(err);
    }
  })
});
``
router.get('/tempdata',(req,res)=>{
  var lis=Array()
  con.query('select * from fire_fighter',(err,rows)=>{
    console.log(rows[0])
    lis.push(rows[0]);
    con.query('select * from fire_station',(err,rows2)=>{
      console.log(rows2[0]);
      lis.push(rows2[0])
      console.log(lis);
      res.send(lis);
    })
  });
});

router.get('/mai', (req, res) => {
  // Check if the user is logged in
  console.log(req.session.fire_fighter.id);
  if (req.session.fire_fighter) {
     res.send("welcome"+req.session.fire_fighter.id);
  }
  // Otherwise, redirect to the login page
  res.redirect('/');
});

//poll
router.get('/checkpoll',(req,res)=>{
  con.query('select *from location where status="fire"',(err,rows,fields)=>{
    if(!err){
      res.send(rows);
    }else{
      console.log(err);
    }
  })
})

// fire detection
router.get('/alarm',(req,res)=>{
  console.log("fire recived");
  res.sendStatus(200);
})
module.exports = router;
