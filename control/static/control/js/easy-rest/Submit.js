let post_location = window.location.href;

if (!post_location.endsWith("/"))
    post_location = post_location += "/";
let handler = new RequestHandler(post_location);

var PostHandler = new PostHandler();

let afterPost = function (data) {
    if (typeof (data) === "string") {
        try {
            data = JSON.parse(data);

        }
        catch (err) {
            return;
        }
    }
    if ('status' in data) {
        if (data.status === "post-failure")
            PostHandler.PostError(data);
        else if (data.status === 'success')
            PostHandler.postSuccess(data);
    }
    if ('alert' in data) {
        PostHandler.Alert(data.alert.type, data.alert.message);
    }
};


function easyRestSubmit(event) {
    event.preventDefault();
    handler.SendAsync($(event.target).serialize(), afterPost, afterPost);

}