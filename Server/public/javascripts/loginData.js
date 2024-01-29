
var userdata={};

function getuserdata(){
  fetch('/userdata')
  .then(response => {
    if (response.status === 200) {
      return response.json();
    } else {
      console.error('Error receiving update from server.');
    }
  })
  .then(data => {
     console.log(data.id);
  })
  .catch(error => {
    console.error(error);
  });
}
getuserdata();

console.log(userdata)

class Data{
    address_line;
    pincode;
    district;
    state;
    location_id;
    time;
    status;
    city;
    report;
    action;
    constructor(address_line,pincode,district,state,location_id,time,status,city,report){
        this.address_line =address_line;
        this.pincode = pincode;
        this.district = district;
        this.state = state;
        this.location_id = location_id;
        this.time = time;
        this.status = status;
        this.city = city;
        this.report = report;
        this.createRow();
    }
    createRow(){
        const table = document.querySelector('.page-login-data');
        /*Create row*/
        const row = document.createElement('div');
        row.classList.add('data-row');
        /*create columns*/
        const addressLine = document.createElement('div');
        const pincode = document.createElement('div');
        const district = document.createElement('div');
        const state = document.createElement('div');
        const location_id = document.createElement('div');
        const time = document.createElement('div');
        const status = document.createElement('div');
        const city = document.createElement('div');
        const report = document.createElement('div');
        const action = document.createElement('div');
        /*create text elements for each column and assign values*/
        const addressLineText = document.createElement('span');
        addressLineText.innerText = this.address_line;
        const pincodeText = document.createElement('span');
        pincodeText.innerText = this.pincode;
        const districtText = document.createElement('span');
        districtText.innerText = this.district;
        const stateText = document.createElement('span');
        stateText.innerText = this.state;
        const locationIdText = document.createElement('span');
        locationIdText.innerText = this.location_id;
        const timeText = document.createElement('span');
        timeText.innerText = this.time;
        const statusText = document.createElement('span');
        statusText.innerText = this.status;
        const cityText = document.createElement('span');
        cityText.innerText = this.city;
        const reporText = document.createElement('span');
        reporText.innerText = this.report;
        const actionText = document.createElement('button');
        actionText.style.display = 'none';
        /*In case of fire take action should appear*/
        if(statusText.innerText === 'fire'){
            console.log('fire');
            row.style.color = 'red';
            actionText.style.display = 'inline-block';
            actionText.style.color ='red';            
            actionText.innerText  = 'Take Action';
            action.addEventListener('click',(e)=>{
                this.takeAction(this);

        })
        }
        if(statusText.innerText === 'under_maintainance'){
          console.log('um');
          row.style.color = 'orange';
          actionText.style.display = 'inline-block';
          actionText.style.color ='orange';            
          actionText.innerText  = 'Finish';
          action.addEventListener('click',(e)=>{
              this.finsh(this);

      })
      }
      if(statusText.innerText==='under_control'){
        row.style.color = 'green';
      }
        /* append columnValues to columns*/
        addressLine.append(addressLineText);
        pincode.append(pincodeText);
        district.append(districtText);
        state.append(stateText);
        location_id.append(locationIdText);
        time.append(timeText);
        status.append(statusText);
        city.append(cityText);
        report.append(reporText);
        action.append(actionText);
        /*append columns to the row */
        row.append(addressLine);
        row.append(pincode);
        row.append(district);
        row.append(state);
        row.append(location_id);
        row.append(time);
        row.append(status);
        row.append(city);
        row.append(report);
        row.append(action);
        /*Append row to table*/
        table.append(row);    
    }
    finsh(obj){
      console.log(obj);
      fetch('/finish', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(obj)
      })
      .then(response => response.json())
      .then(data => console.log(data))
      .catch(error => console.error(error));
    }
    takeAction(obj){
        console.log(obj);
        fetch('/maintain', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(obj)
        })
        .then(response => response.json())
        .then(data => console.log(data))
        .catch(error => console.error(error));
    }
}
let idata=[]
function showrecords(data){
    if(idata.length==0 ){
      idata=data;
      idata.forEach((ele)=>{            
      new Data(ele.address_line,ele.pincode,ele.district,ele.state,ele.location_id,ele.time,ele.status,ele.city,ele.report);
     });
    }else if(idata.length!=0 && !(JSON.stringify(idata) === JSON.stringify(data))){
      console.log('heyyyy')
      location.reload();
    }
    

}
function requestStatus() {
    fetch('/status')
      .then(response => {
        if (response.status === 200) {
          return response.json();
        } else {
          console.error('Error receiving update from server.');
        }
      })
      .then(data => {
        // console.log(data);
        showrecords(data)


      })
      .catch(error => {
        console.error(error);
      });
  }
  setInterval(requestStatus, 1000);
//   console.log(c)
//   c.forEach((ele)=>{
//     new Data(ele.address_line,ele.pincode,ele.district,ele.state,ele.device_id,ele.time,ele.status,ele.city,ele.report);
// });
