function parseResponse(response) {
  switch (response.status) {
    case "ok":
      if (response.hasOwnProperty("position")) {
        console.log(response.position);
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

    // X axis
    jogAttachOnClick("#xUp", (distance, speed) => {
      return { x: distance, speed: speed };
    });
    jogAttachOnClick("#xDown", (distance, speed) => {
      return { x: -distance, speed: speed };
    });

    // Y axis
    jogAttachOnClick("#yUp", (distance, speed) => {
      return { y: distance, speed: speed };
    });
    jogAttachOnClick("#yDown", (distance, speed) => {
      return { y: -distance, speed: speed };
    });

    parkAttachOnClick("#xyPark", speed => {
      return { axis: "xy", speed: speed };
    });

    // Z axis
    jogAttachOnClick("#zUp", (distance, speed) => {
      return { z: distance, speed: speed };
    });
    jogAttachOnClick("#zDown", (distance, speed) => {
      return { z: -distance, speed: speed };
    });

    parkAttachOnClick("#zPark", speed => {
      return { axis: "z", speed: speed };
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
