function setState(vars) {
  id = vars['bet_state'];
  if (id != "") {
    document.getElementById(id).className = 'active';
  }
  goal_state = vars['goal_state']
  if(goal_state != "") {
    goals = goal_state.split(" : ")
    document.getElementById("T1").value = goals[0];
    document.getElementById("T2").value = goals[1];
  }
};

function heartbeat() {
  var poll=new XMLHttpRequest();
  poll.open("POST", "/set_heartbeat_time");
  poll.send();
};
