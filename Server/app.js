var createError = require('http-errors');
var express = require('express');
var expresslongpoll = require("express-longpoll")(app)
var longpollWithDebug = require("express-longpoll")(express, { DEBUG: true })
const session = require('express-session');
const MySQLStore = require('express-mysql-session')(session);
var path = require('path');
var cookieParser = require('cookie-parser');
var logger = require('morgan');
var mysql=require('mysql')


var indexRouter = require('./routes/index');
var usersRouter = require('./routes/users');
var sqlcon=require("./routes/sql.js");

var app = express();

const sessionStore = new MySQLStore({
  expiration: (1825 * 86400 * 1000), // cookie expires in 5 years
  endConnectionOnClose: false,
  createDatabaseTable: true,
  schema: {
    tableName: 'sessions',
    columnNames: {
      session_id: 'session_id',
      expires: 'expires',
      data: 'data'
    }
  }

}, sqlcon);

// Use express-session to manage sessions
app.use(session({
  key: 'session_cookie_name',
  secret: 'session_cookie_secret',
  store: sessionStore,
  resave: false,
  saveUninitialized: false
}));

// view engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'ejs');

app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));

app.use('/', indexRouter);
app.use('/users', usersRouter);

// catch 404 and forward to error handler
app.use(function(req, res, next) {
  next(createError(404));
});

// error handler
app.use(function(err, req, res, next) {
  // set locals, only providing error in development
  res.locals.message = err.message;
  res.locals.error = req.app.get('env') === 'development' ? err : {};

  // render the error page
  res.status(err.status || 500);
  res.render('error');
});

module.exports = app;
app.listen(3000);