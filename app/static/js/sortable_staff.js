export function sortableStaff() {
    const observer = new MutationObserver(function (mutations) {
      mutations.forEach(function (mutation) {
        mutation.target.querySelectorAll("li .label").forEach(elem => {
        if (mutation.target.classList.contains('ghost')) {
          elem.classList.remove("col-3");
        } else {
          elem.classList.add("col-3");
        }
        });
      });
    });

    document.querySelectorAll('#feature-container li')
      .forEach(elem => {observer.observe(elem, {
        attributes: true,
        attributeFilter: ['class']
      });
    });

    document.querySelectorAll("#feature-container ul")
      .forEach(ul => {
        new Sortable(ul, {
          animation:150,
          group: "features",
          ghostClass: "ghost",
          handle: ".draghandle",
          onEnd: function(evt) {
            if (evt.oldIndex !== evt.newIndex || evt.from.id !== evt.to.id) {
              // Trigger htmx to send information to the server
              evt.item.classList.add("ghost")
              htmx.ajax("POST", "update-table", {
                target: "#model-container",
                values: {
                  type: "feature",
                  from: evt.oldIndex,
                  to: evt.newIndex,
                  feature: evt.item.dataset.feature,
                  fromList: evt.from.id,
                  toList: evt.to.id,
                }
              });
            }
          }
        });
      });
}