function CMSNewsList () {

}

CMSNewsList.prototype.initDatePicker = function () {
    var startPicker = $('#start-picker');
    var endPicker = $('#end-picker');

    var todayDate = new Date();
    var todayStr = todayDate.getFullYear() + '/' + (todayDate.getMonth()+1) + '/' + todayDate.getDate();
    var options = {
        'showButtonPanel': true,
        'format': 'yyyy/mm/dd',
        'startDate': '2017/4/21',
        'endDate': todayStr,
        'language':'zh-CN',
        'todayBtn': 'linked',
        'todayHighlight': true,
        'clearBtn': true,
        'autoclose': true
    };
    startPicker.datepicker(options);
    endPicker.datepicker(options);
};


CMSNewsList.prototype.listenDeleteEvent = function () {
    var deleteBtn = $('.submit-delete-btn');
    var news_id = $(this).attr('data-news-id');
    console.log(news_id);

    deleteBtn.click(function () {
        xfzalert.alertConfirm({
            'text':'是否要删除这篇新闻？',
            'confirmCallback':function () {
                xfzajax.post({
                    'url': '/cms/delete_news/',
                    'data':{
                        'news_id':news_id
                    },
                    'success':function (result) {
                        if(result['code'] === 200){
                            window.location = window.location.href;
                        }
                    }
                });
            }
        });
    });
};


CMSNewsList.prototype.run = function () {
    var self = this;
    self.initDatePicker();
    self.listenDeleteEvent()
};

$(function () {
    var newsList = new CMSNewsList();
    newsList.run();
});