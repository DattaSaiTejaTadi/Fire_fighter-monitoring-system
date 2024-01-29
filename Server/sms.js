const accountSid = "ACdacf8b9b01a8457897f793a8b67c17e6";
const authToken = "1baeaebaa817d54ee661d5addc8304ea";
const client = require('twilio')(accountSid, authToken);

client.calls.create({
  twiml: '<Response><Say >hi gorri mawa, nee gf ela undi   </Say></Response>',
  to: '+919390708916',
  from: '+12183955753'
})
.then(call => console.log(call.status));