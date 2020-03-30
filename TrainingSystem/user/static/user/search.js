function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');
var course = [];
$(document).ready(function () {
    $("#txtSearch").autocomplete({
        minLength: 1,
        source: function (request, response) {
            // Fetch data
            var form = $('#search-form');
            $.ajax({
                headers: {
                    "X-CSRFToken": csrftoken
                },
                url: "/user/ajax_calls/search/",
                type: 'post',
                dataType: "json",
                data: form.serialize(),
                success: function (data) {
                    course = [];
                    data.forEach(function myFunction(item, index) {
                        var dict = {};
                        dict.title = item[0];
                        dict.url = item[1];
                        course.push(dict)
                    });
                    response(course);
                }
            });
        },
        focus: function (event, ui) {
            $("txtSearch").val(ui.item.title);
            return false;
        },
        select: function (event, ui) {
            $("#txtSearch").val(ui.item.title);
            return false;
        }
    })
        .autocomplete("instance")._renderItem = function (ul, item) {
        ul.attr("class", "dropdown-menu");
        return $("<li class=\"dropdown-item\" style='padding: 8px 0px;'>")
            .append("<a href='" + item.url + "'>" + item.title + "</a>")
            .appendTo(ul)
    }
});
