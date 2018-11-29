const API = (() => {
  function getPosition(success, fail) {
    $.ajax({
      url: "http://192.168.100.10:5000/api/position/"
    })
      .done(success)
      .fail(fail);
  }

  function updatePosition(position, success, fail) {
    $.ajax({
      url: "http://192.168.100.10:5000/api/position/",
      type: "put",
      data: JSON.stringify(position),
      headers: {
        "x-auth-token": localStorage.accessToken,
        "Content-Type": "application/json"
      },
      dataType: "json"
    })
      .done(success)
      .fail(fail);
  }

  return {
    getPosition: getPosition,
    updatePosition: updatePosition
  };
})();

const MACHINE_CONTROLS = (api => {
  // current_position = null;

  function jogOnClick(id, operation) {
    $(id).on("click", function(event) {
      $(this).blur();
      const distance = parseFloat($("#distanceRangeValue").val()); // get distance slider value
      const speed = parseFloat($("#speedRangeValue").val()); // get speed slider value
      // get current position
      api.getPosition(
        position => {
          console.log(position);
          position = operation(position, distance, speed);
          console.log(position);
          api.updatePosition(
            position,
            () => {},
            error => {
              alert("Failed to update position");
            }
          );
        },
        error => {
          alert("Error getting current position");
        }
      );
    });
  }

  function attachOnClickHandlers() {
    $("#home").on("click", function(event) {
      $(this).blur();
      updatePosition();
    });

    jogOnClick("#jogUp", (position, distance, speed) => {
      position.y += distance;
      return position;
    });
    jogOnClick("#jogDown", (position, distance, speed) => {
      position.y -= distance;
      return position;
    });
    jogOnClick("#jogRight", (position, distance, speed) => {
      position.x += distance;
      return position;
    });
    jogOnClick("#jogLeft", (position, distance, speed) => {
      position.x -= distance;
      return position;
    });
  }

  function attachOnChangeHandlers() {
    $("#distanceRange").on("change", function(event) {
      $("#distanceRangeValue").val($(this).val());
    });
    $("#speedRange").on("change", function(event) {
      $("#speedRangeValue").val($(this).val());
    });
  }

  function initSliderValues() {
    $("#distanceRangeValue").val($("#distanceRange").val());
    $("#speedRangeValue").val($("#speedRange").val());
  }

  function init() {
    attachOnClickHandlers();
    attachOnChangeHandlers();
    initSliderValues();
  }

  return {
    init: init
  };
})(API);

function displayJobDetails(name) {
  $.ajax({
    url: "http://192.168.100.10:5000/api/job/" + name
  }).then(data => {
    let tbody = $($("#jobDetails").find("tbody"));
    tbody.empty();
    $.each(data, function(index, value) {
      let tr = $("<tr>");
      tr.append('<th scope="row">' + value.name + "</th>");
      tr.append("<td>" + value.value + "</td>");
      tr.append("<td>" + value.package + "</td>");
      tr.append("<td>" + value.x + "</td>");
      tr.append("<td>" + value.y + "</td>");
      tr.append("<td>" + value.angle + "</td>");
      tr.append("<td>" + value.type + "</td>");
      // add onclick handler
      tr.on("click", () => {
        diplayJob(value.name);
      });
      tbody.append(tr);
    });
    $("#jobDetails").removeClass("d-none");
  });
}

// function displayJobList() {
//   $.ajax({
//     url: "http://192.168.100.10:5000/api/job"
//   }).then(data => {
//     let tbody = $($("#jobTable").find("tbody"));
//     tbody.empty();
//     $.each(data, function(index, value) {
//       let tr = $("<tr>");
//       tr.append('<th scope="row">' + value.name + "</th>");
//       tr.append("<td>" + value.length + "</td>");
//       tr.append("<td>" + value.width + "</td>");
//       tr.append("<td>" + value.x + "</td>");
//       tr.append("<td>" + value.y + "</td>");
//       tr.append("<td>" + value.angle + "</td>");
//       // add onclick handler
//       tr.on("click", () => {
//         tbody
//           .find(".table-active")
//           .each((index, element) => $(element).removeClass("table-active"));
//         tr.addClass("table-active");
//         displayJobDetails(value.name);
//       });
//       tbody.append(tr);
//     });
//   });
// }

// function displayJobSelectorOptions() {
//   $.ajax({
//     url: "http://192.168.100.10:5000/api/job"
//   }).then(data => {
//     let select = $("#jobSelector");
//     select.empty();
//     select.append("<option selected disabled>Choose...</option>");
//     $.each(data, function(index, value) {
//       select.append("<option>" + value + "</option>");
//     });
//     select.on("change", event => {
//       displayJobDetails(select.val());
//       // event.preventDefault();
//       select.blur();
//     });
//   });
// }

const JOB = (() => {
  function displayJobList(list, socket) {
    let select = $("#jobSelector");
    select.empty();
    select.append("<option selected disabled>Choose...</option>");
    $.each(list, function(index, value) {
      select.append("<option>" + value + "</option>");
    });
    select.on("change", event => {
      socket.emit("get_job_details", select.val());
      select.blur();
    });
  }

  function displayJobDetails(data) {
    let tbody = $($("#jobDetails").find("tbody"));
    tbody.empty();
    $.each(data, function(index, value) {
      let tr = $("<tr>");
      tr.append('<th scope="row">' + value.name + "</th>");
      tr.append("<td>" + value.value + "</td>");
      tr.append("<td>" + value.package + "</td>");
      tr.append("<td>" + value.x + "</td>");
      tr.append("<td>" + value.y + "</td>");
      tr.append("<td>" + value.angle + "</td>");
      tr.append("<td>" + value.type + "</td>");
      // add onclick handler
      tr.on("click", () => {
        // diplayJob(value.name);
      });
      tbody.append(tr);
    });
    $("#jobDetails").removeClass("d-none");
  }

  function init(socket) {
    socket.on("job_list", function(data) {
      displayJobList(data, socket);
    });

    socket.on("job_details", function(data) {
      displayJobDetails(data);
    });
  }

  function updateJobList(socket) {
    socket.emit("get_job_list");
  }

  function updateJobDetails(socket) {
    socket.emit("get_job_list");
  }

  return {
    init: init,
    updateJobList: updateJobList,
    updateJobDetails: updateJobDetails
  };
})();

$(document).ready(function() {
  var socket = io.connect("/");

  socket.on("connect", function() {
    JOB.init(socket);
    JOB.updateJobList(socket);
  });

  socket.on("log", function(msg) {
    $("#logTextarea").append(msg.toString() + "\n");
  });

  $("#uploadJob").on("click", function(event) {
    // alert("Hello! I am an alert box!!");
  });

  // displayJobSelectorOptions();

  MACHINE_CONTROLS.init();
});
