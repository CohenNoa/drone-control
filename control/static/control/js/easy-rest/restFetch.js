window.contextUpdateInterval = 3000;
function RestFetch(){

    this.apis = {}
    this.fetchIntervalId = null;

    this.beforeFormatHtml = {};


    this.stopFetch = function(){
        return clearInterval(this.fetchIntervalId);
    }

    this.fetch = function(){
     optimized = {};
     $(".fetch-context").each(function(){
            let element = $(this);
            let url = element.data("fetch-url");
            url = url === undefined ? window.location.pathname : url;
            if(!(url in currentPageContextFetcher.apis)){
                currentPageContextFetcher.apis[url] = new RequestHandler(url);
            }
            if(!(url in optimized))
                optimized[url] = [];

            optimized[url].push(element);

        });

      for(url in optimized){
            let currentApi = currentPageContextFetcher.apis[url]
            // optimize send more then one element for the same url
            currentApi.SendAsync({"action":"fetch-content"}, currentPageContextFetcher.formatData,
            function(error){console.warn("fetchable error", error)},
            {"elements":optimized[url]});
      }

    };

    this.formatData = function(context){
        let elements = context['elements'];
        for(let element of elements){
            let elementId = element.attr("id");
            if(elementId === undefined){
                elementId = randomId();
                element.attr("id", elementId);
            }
            if(! (elementId in currentPageContextFetcher.beforeFormatHtml))
                currentPageContextFetcher.beforeFormatHtml[elementId] = element.html();

            let html = "";
            html = currentPageContextFetcher.beforeFormatHtml[elementId];
            for(key in context){

                html = html.replace("{"+key+"}", context[key]);
            }

            element.html(html);
        }



    };

    this.bind = function(){

        this.fetchIntervalId = setInterval(this.fetch, window.contextUpdateInterval);
    }


}

var currentPageContextFetcher = new RestFetch();

$(document).ready(function(){

    // this script will bind only for pages with the fetch context class
    if($(".fetch-context").length > 0)
    {
        // first fetch
        currentPageContextFetcher.fetch();

        // always fetch
        currentPageContextFetcher.bind();
    }

});

function randomId() {
  function s4() {
    return Math.floor((1 + Math.random()) * 0x10000)
      .toString(16)
      .substring(1);
  }
  return s4() + s4()  + s4() + s4() +
    s4() +  s4() + s4() + s4();
}