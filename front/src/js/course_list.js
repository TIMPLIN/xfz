function CMSCourseList () {

}

CMSCourseList.prototype.initDatePicker = function () {
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

CMSCourseList.prototype.listenDeleteEvent = function () {
    var deleteBtn = $('.delete-course');
    var course_id = $(this).attr('data-course-id');

    deleteBtn.click(function () {
        xfzalert.alertConfirm({
            'text':'是否要删除这篇新闻？',
            'confirmCallback':function () {
                xfzajax.post({
                    'url': '/cms/delete_course/',
                    'data':{
                        'course_id':course_id
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

CMSCourseList.prototype.run = function () {
    var self = this;
    self.initDatePicker();
    self.listenDeleteEvent()
};

$(function () {
    var CourseList = new CMSCourseList();
    CourseList.run();
});