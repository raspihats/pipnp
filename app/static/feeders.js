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

const FEEDERS = (() => {
  let feedersSocket;

  function accordionCard() {}

  function displayFeedersTable() {
    feedersSocket.emit("get", "all", feeders => {
      let feedersTable = $("#feedersTable");
      let tbody = $(feedersTable.find("tbody"));
      tbody.empty();
      $.each(feeders, function(index, feeder) {
        let component_details = "";
        let component_attributes = ["value", "voltage", "tolerance", "package"];
        component_attributes.forEach(function(attribute) {
          if (feeder.component.hasOwnProperty(attribute)) {
            component_details += " " + feeder.component[attribute];
          }
        });

        let tr = $('<tr style="cursor: pointer;">');
        tr.append('<th scope="row">' + feeder.name + "</th>");
        tr.append("<td>" + feeder.type + "</td>");
        tr.append("<td>" + component_details + "</td>");
        tr.append("<td>" + feeder.size + "</td>");
        tr.append("<td>" + feeder.remaining + "</td>");
        tr.append(
          "<td>{" +
            feeder.point.x +
            ", " +
            feeder.point.y +
            ", " +
            feeder.point.z +
            "}</td>"
        );
        tbody.append(tr);
      });
      feedersTable.removeClass("d-none");
    });
  }

  function init(socket) {
    feedersSocket = socket;
    // displayFeedersTable();
  }

  return {
    init: init
  };
})();

export default FEEDERS;
