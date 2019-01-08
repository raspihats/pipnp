function parseResponse(response) {
  switch (response.status) {
    case "ok":
      if (response.hasOwnProperty("position")) {
        // console.log(response.position);
      }
      break;
    case "error":
      alert("ERROR: " + response.message);
      break;
  }
}

const MACHINE_CONTROLS = (() => {
  let positionSocket;

  function jogAttachOnClick(id, operation) {
    $(id).on("click", function(event) {
      $(this).blur();
      const distance = parseFloat($("#distanceRangeValue").val()); // get distance slider value
      const speed = parseFloat($("#speedRangeValue").val()); // get speed slider value
      positionSocket.emit("jog", operation(distance, speed), response => {
        parseResponse(response);
      });
    });
  }

  function parkAttachOnClick(id, operation) {
    $(id).on("click", function(event) {
      $(this).blur();
      const distance = parseFloat($("#distanceRangeValue").val()); // get distance slider value
      const speed = parseFloat($("#speedRangeValue").val()); // get speed slider value
      positionSocket.emit("park", operation(speed), response => {
        parseResponse(response);
      });
    });
  }

  function attachOnClickHandlers() {
    $("#home").on("click", function(event) {
      $(this).blur();
      positionSocket.emit("home", function(position) {});
    });

    $("#pump").on("click", function(event) {
      $(this).blur();
      actuatorsSocket.emit("toggle", "pump", function(data) {});
    });

    // X axis
    jogAttachOnClick("#xUp", (distance, speed) => {
      return { x: distance, speed_factor: speed / 100.0 };
    });
    jogAttachOnClick("#xDown", (distance, speed) => {
      return { x: -distance, speed_factor: speed / 100.0 };
    });

    // Y axis
    jogAttachOnClick("#yUp", (distance, speed) => {
      return { y: distance, speed_factor: speed / 100.0 };
    });
    jogAttachOnClick("#yDown", (distance, speed) => {
      return { y: -distance, speed_factor: speed / 100.0 };
    });

    parkAttachOnClick("#xyPark", speed => {
      return { axis: "xy", speed_factor: speed / 100.0 };
    });

    // Z axis
    jogAttachOnClick("#zUp", (distance, speed) => {
      return { z: distance, speed_factor: speed / 100.0 };
    });
    jogAttachOnClick("#zDown", (distance, speed) => {
      return { z: -distance, speed_factor: speed / 100.0 };
    });

    parkAttachOnClick("#zPark", speed => {
      return { axis: "z", speed_factor: speed / 100.0 };
    });

    // A axis
    jogAttachOnClick("#aCcw", (distance, speed) => {
      return { a: distance, speed_factor: speed / 100.0 };
    });
    jogAttachOnClick("#aCw", (distance, speed) => {
      return { a: -distance, speed_factor: speed / 100.0 };
    });

    parkAttachOnClick("#aPark", speed => {
      return { axis: "a", speed_factor: speed / 100.0 };
    });

    // B axis
    jogAttachOnClick("#bCcw", (distance, speed) => {
      return { b: distance, speed_factor: speed / 100.0 };
    });
    jogAttachOnClick("#bCw", (distance, speed) => {
      return { b: -distance, speed_factor: speed / 100.0 };
    });

    parkAttachOnClick("#bPark", speed => {
      return { axis: "b", speed_factor: speed / 100.0 };
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

  function init(socket) {
    positionSocket = socket;
    attachOnClickHandlers();
    attachOnChangeHandlers();
    initSliderValues();
  }

  return {
    init: init
  };
})();

export default MACHINE_CONTROLS;
