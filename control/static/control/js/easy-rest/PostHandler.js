function PostHandler() {

    this.postSuccess = function (data) {
    };

    this.PostError = function (data) {
        if ("form_errors" in data) {
            let errors = data.form_errors;
            if (typeof(errors) === "object") {
                for (let key in errors) {
                    this.HandleErrors(key, errors[key]);
                }
            }
        }
    };

    this.HandleErrors = function (element_id, message) {
        $("#error_handler_post" + element_id).remove();
        $("#id_" + element_id).before("<p id='error_handler_post" + element_id + "' style='color:red'>" + message + "</p>")
    };

    this.Alert = function (type, message) {
        $("#current_post_message").remove();
        $("body").prepend("<div id ='current_post_message' class='alert alert-" + type + "'>" +
            "<!--This alert requires bootstrap, to change ui handling of post declare a new PostHandler-->"
            + message +
            "</div>")
    };

}