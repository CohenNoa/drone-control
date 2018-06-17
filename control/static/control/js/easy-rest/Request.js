function RequestHandler(url) {

    this.url = url;
    /**
     * on failure returns {"error":"error value"}
     * @return {object}
     */
    this.SendSync = function (data) {
        let ajax_response = undefined;
        $.ajax(
            {
                async: false,
                url: this.url,
                type: 'POST',
                data: data,
                headers: {"X-CSRFToken": getCsrf()},

                success: function (jsonResponse) {
                    ajax_response = jsonResponse;


                },
                error: function (error) {
                    ajax_response = {"error": error}

                }
            });
        return ajax_response;

    };

    this.SendAsync = function (data, OnSuccess, OnError = function (error) {
    }, additionalSuccessData = {}) {

        $.ajax(
            {
                async: true,
                url: this.url,
                type: 'POST',
                data: data,
                headers: {"X-CSRFToken": getCsrf()},

                success: function (data) {
                    let functionData = data;
                    try {
                        functionData = JSON.parse(functionData);
                    }
                    catch (err) {

                    }
                    for (key in additionalSuccessData) {
                        functionData[key] = additionalSuccessData[key];
                    }
                    OnSuccess(functionData);
                },
                error: OnError
            });

    };
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        let cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function getCsrf() {
    return getCookie("csrftoken")
}