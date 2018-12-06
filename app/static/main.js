import MACHINE_CONTROLS from "./machine_controls.js";

// const API = (() => {
//   let sockets;

//   function getPosition() {
//     sockets.position.emit("get", null, function(position) {
//       position = operation(position, distance, speed);
//       console.log("get" + position.toString());
//       socket.emit("update", null, function(position) {
//         console.log(position);
//       });
//     });
//   }

//   function init(sock) {
//     sockets = sock;
//   }

//   return {
//     init: init
//   };
// })();

const GUI = (() => {
  let sockets;

  function displayJobList() {
    sockets.job.emit("get", "all", list => {
      let select = $("#jobSelector");
      select.empty();
      select.append("<option selected disabled>Choose...</option>");
      $.each(list, function(index, value) {
        select.append("<option>" + value + "</option>");
      });
      select.on("change", event => {
        displayJobSteps(select.val());
        select.blur();
      });
    });
  }

  function displayStepButtons(type) {
    const button = $("<button/>", {
      type: "button",
      class: "btn btn-outline-secondary px-1 py-0",
      id: "removeJobStep",
      "data-toggle": "tooltip",
      "data-placement": "top",
      title: "Remove job step"
    });

    const icon = $('<i class="fas fa-trash fa-sm"></i>');
    icon.appendTo(button);
    return button;
  }

  function displayTypeSelector(selectedValue, onChange) {
    const select = $("<select/>", {
      class: "form-control form-control-sm px-1 py-0"
      // id: name + "TypeSelector"
    });

    const options = ["origin", "fiducial", "component", "ignore"];
    $.each(options, (index, value) => {
      const option = $('<option class="">' + value + "</option>");
      if (value == selectedValue) {
        option.prop("selected", true);
      }
      select.append(option);
    });

    select.on("change", () => {
      onChange(select);
    });

    return select;
  }

  function displayJobSteps(name) {
    sockets.job.emit("get", name, steps => {
      if (!(Array.isArray(steps) && steps.length > 0)) {
        alert("Error loading job file '" + name + "'.");
        $("#jobSelector").prop("selectedIndex", 0);
        $("#jobSteps").addClass("d-none");
        return;
      }
      // display buttons
      $("#addJobStep").removeClass("d-none");
      $("#removeJobStep").removeClass("d-none");

      // populate table
      let tbody = $($("#jobSteps").find("tbody"));
      tbody.empty();
      $.each(steps, function(index, step) {
        let tr = $('<tr style="cursor: pointer;">');
        tr.append('<th scope="row">' + step.name + "</th>");
        tr.append("<td>" + step.value + "</td>");
        tr.append("<td>" + step.package + "</td>");
        tr.append("<td>" + step.x + "</td>");
        tr.append("<td>" + step.y + "</td>");
        tr.append("<td>" + step.angle + "</td>");

        // tr.append("<td>" + step.type + "</td>");
        let td = $("<td/>", {
          class: "py-0"
        });
        td.append(
          displayTypeSelector(step.type, select => {
            step.type = select.val();
            sockets.job.emit("update", name, steps);
            // displayJobSteps(name);
          })
        );
        tr.append(td);

        td = $("<td/>");
        td.append(displayStepButtons(step.type));

        // add onclick handler
        tr.on("click", () => {
          $.each(tbody.children(), function(index, element) {
            $(element).removeClass("table-active");
          });
          tr.addClass("table-active");
          $("#removeJobStep").prop("disabled", false);
          $("#removeJobStep").on("click", function(event) {
            $(this).blur();
            var filtered = steps.filter(
              st => JSON.stringify(step) != JSON.stringify(st)
            );
            console.log(filtered);
            sockets.job.emit("update", name, filtered);
            displayJobSteps(name);
          });
        });
        tbody.append(tr);
      });
      $("#jobSteps").removeClass("d-none");
    });
  }

  function init(sock) {
    sockets = sock;
    displayJobList();

    // $("#startJob").on("click", function(event) {
    //   $(this).blur();
    //   socket.emit("start_job", $("#jobSelector").val());
    // });
  }

  return {
    init: init
  };
})();

$(document).ready(function() {
  var sockets = {
    main: io.connect("/"),
    position: io.connect("/position"),
    job: io.connect("/job")
  };

  sockets.main.on("log", function(msg) {
    $("#logTextarea").append(msg.toString() + "\n");
  });

  MACHINE_CONTROLS.init(sockets.position);

  sockets.position.on("connect", function() {
    GUI.init(sockets);
  });

  $("#uploadJob").on("click", function(event) {
    // alert("Hello! I am an alert box!!");
  });

  // displayJobSelectorOptions();
});
